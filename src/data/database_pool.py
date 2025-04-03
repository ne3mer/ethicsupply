#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import pandas as pd
from datetime import datetime
import threading
import time
import logging
from queue import Queue
from contextlib import contextmanager
import numpy as np

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('EthicSupply.Database')

class ConnectionPool:
    """A simple connection pool for SQLite databases."""
    
    def __init__(self, db_path, max_connections=5):
        """Initialize the connection pool.
        
        Args:
            db_path (str): Path to the database file.
            max_connections (int, optional): Maximum number of connections. Defaults to 5.
        """
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = Queue(maxsize=max_connections)
        self.lock = threading.Lock()
        
        # Initialize the pool with connections
        for _ in range(max_connections):
            conn = sqlite3.connect(db_path, timeout=120.0)
            cursor = conn.cursor()
            # Enable WAL mode for better concurrency
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA busy_timeout=120000")
            cursor.close()
            self.connections.put(conn)
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool.
        
        Yields:
            sqlite3.Connection: A database connection.
        """
        conn = None
        try:
            conn = self.connections.get(timeout=60.0)
            yield conn
        finally:
            if conn:
                self.connections.put(conn)
    
    def close_all(self):
        """Close all connections in the pool."""
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()

class Database:
    """SQLite database for storing supplier data and optimization history."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path='ethicsupply_wal.db'):
        """Singleton pattern to ensure only one database instance exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.db_path = os.path.join(os.path.dirname(__file__), db_path)
                cls._instance.connection_pool = ConnectionPool(cls._instance.db_path)
                cls._instance._setup_database()
            return cls._instance
    
    def __init__(self, db_path='ethicsupply_wal.db'):
        """Initialize the database.
        
        Args:
            db_path (str, optional): Path to the database file. 
                Defaults to 'ethicsupply_wal.db'.
        """
        pass  # Initialization is done in __new__
    
    def _setup_database(self):
        """Set up the database and create tables."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Create tables
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Enable foreign keys
                cursor.execute("PRAGMA foreign_keys=ON")
                
                # Create suppliers table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS suppliers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        cost REAL NOT NULL,
                        co2 REAL NOT NULL,
                        delivery_time REAL NOT NULL,
                        ethical_score REAL NOT NULL
                    )
                ''')
                
                # Create optimizations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS optimizations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        description TEXT,
                        num_suppliers INTEGER NOT NULL
                    )
                ''')
                
                # Create optimization_results table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS optimization_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        optimization_id INTEGER NOT NULL,
                        supplier_id INTEGER NOT NULL,
                        score REAL NOT NULL,
                        selected INTEGER NOT NULL,
                        FOREIGN KEY (optimization_id) REFERENCES optimizations (id),
                        FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
                    )
                ''')
                
                # Create activities table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS activities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        activity_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        details TEXT
                    )
                ''')
                
                conn.commit()
                logger.info("Database tables created successfully")
            finally:
                cursor.close()
    
    def save_suppliers(self, suppliers_df):
        """Save suppliers to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data.
            
        Returns:
            list: List of supplier IDs.
        """
        logger.info(f"Saving {len(suppliers_df)} suppliers")
        
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            supplier_ids = []
            
            try:
                # Start transaction
                cursor.execute("BEGIN")
                
                for _, row in suppliers_df.iterrows():
                    cursor.execute('''
                        INSERT INTO suppliers (name, cost, co2, delivery_time, ethical_score)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        row['name'],
                        row['cost'],
                        row['co2'],
                        row['delivery_time'],
                        row['ethical_score']
                    ))
                    supplier_ids.append(cursor.lastrowid)
                
                # Commit transaction
                conn.commit()
                logger.info(f"Successfully saved {len(supplier_ids)} suppliers")
                return supplier_ids
            except Exception as e:
                # Rollback transaction on error
                conn.rollback()
                logger.error(f"Error saving suppliers: {e}")
                raise e
            finally:
                cursor.close()
    
    def get_suppliers(self):
        """Get all suppliers from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing supplier data.
        """
        logger.info("Fetching all suppliers")
        
        with self.connection_pool.get_connection() as conn:
            try:
                query = "SELECT id, name, cost, co2, delivery_time, ethical_score FROM suppliers"
                df = pd.read_sql_query(query, conn)
                logger.info(f"Retrieved {len(df)} suppliers")
                return df
            except Exception as e:
                logger.error(f"Error getting suppliers: {e}")
                raise e
    
    def save_optimization(self, suppliers_df, description='', method='ml_model'):
        """Save optimization results to the database.
        
        Args:
            suppliers_df (DataFrame): DataFrame with supplier data
            description (str): Description of the optimization
            method (str): Method used for optimization
        
        Returns:
            int: Optimization ID
        """
        conn = None
        try:
            # Create connection and cursor
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # First determine the schema of the optimizations table
            cursor.execute("PRAGMA table_info(optimizations)")
            columns = [info[1] for info in cursor.fetchall()]
            
            timestamp = int(time.time())
            desc = description or f"Optimization run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            num_suppliers = len(suppliers_df)
            
            # Create optimization record based on schema
            optimization_id = None
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='optimizations'")
            if not cursor.fetchone():
                # Create the table with minimal schema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS optimizations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp INTEGER NOT NULL,
                        description TEXT
                    )
                ''')
                cursor.execute('''
                    INSERT INTO optimizations (timestamp, description)
                    VALUES (?, ?)
                ''', (timestamp, desc))
                optimization_id = cursor.lastrowid
            else:
                # Table exists, determine schema
                cols = set(columns)
                
                # Different combinations of columns
                if 'method' in cols and 'num_suppliers' in cols and 'score' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, method, num_suppliers, score)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (timestamp, desc, method, num_suppliers, 0))
                elif 'method' in cols and 'num_suppliers' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, method, num_suppliers)
                        VALUES (?, ?, ?, ?)
                    ''', (timestamp, desc, method, num_suppliers))
                elif 'method' in cols and 'score' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, method, score)
                        VALUES (?, ?, ?, ?)
                    ''', (timestamp, desc, method, 0))
                elif 'num_suppliers' in cols and 'score' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, num_suppliers, score)
                        VALUES (?, ?, ?, ?)
                    ''', (timestamp, desc, num_suppliers, 0))
                elif 'method' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, method)
                        VALUES (?, ?, ?)
                    ''', (timestamp, desc, method))
                elif 'num_suppliers' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, num_suppliers)
                        VALUES (?, ?, ?)
                    ''', (timestamp, desc, num_suppliers))
                elif 'score' in cols:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description, score)
                        VALUES (?, ?, ?)
                    ''', (timestamp, desc, 0))
                else:
                    cursor.execute('''
                        INSERT INTO optimizations (timestamp, description)
                        VALUES (?, ?)
                    ''', (timestamp, desc))
                
                optimization_id = cursor.lastrowid
            
            logging.debug(f"Created optimization with ID {optimization_id}")
            
            # Check if ethical_score exists, otherwise it will be calculated by the model
            if 'ethical_score' not in suppliers_df.columns:
                # Calculate normalized metrics for ethical score
                normalized_df = suppliers_df.copy()
                for col in ['cost', 'co2', 'delivery_time']:
                    min_val = normalized_df[col].min()
                    max_val = normalized_df[col].max()
                    if max_val > min_val:
                        normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
                    else:
                        normalized_df[col] = 0.5
                
                # Invert cost, CO2, and delivery time (lower is better)
                for col in ['cost', 'co2', 'delivery_time']:
                    normalized_df[col] = 1 - normalized_df[col]
                
                # Calculate ethical score
                suppliers_df['ethical_score'] = (
                    normalized_df['cost'] * 0.3 + 
                    normalized_df['co2'] * 0.4 + 
                    normalized_df['delivery_time'] * 0.3
                ) * 100
            
            # Save suppliers to the database (create table if it doesn't exist)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    optimization_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    cost REAL NOT NULL,
                    co2 REAL NOT NULL,
                    delivery_time REAL NOT NULL,
                    ethical_score REAL NOT NULL
                )
            ''')
            
            # Save supplier data
            logging.info(f"Saving {len(suppliers_df)} suppliers")
            for _, row in suppliers_df.iterrows():
                cursor.execute('''
                    INSERT INTO suppliers (
                        optimization_id, name, cost, co2, delivery_time, ethical_score
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    optimization_id,
                    row['name'],
                    float(row['cost']),
                    float(row['co2']),
                    float(row['delivery_time']),
                    float(row['ethical_score'])
                ))
            
            logging.info("Successfully saved suppliers")
            
            # Update score if applicable
            if 'score' in cols and len(suppliers_df) > 0:
                # Save the score of the top supplier
                try:
                    top_supplier = suppliers_df.iloc[0]
                    if 'predicted_score' in top_supplier:
                        cursor.execute('''
                            UPDATE optimizations
                            SET score = ?
                            WHERE id = ?
                        ''', (float(top_supplier['predicted_score']), optimization_id))
                except Exception as e:
                    logging.warning(f"Could not update score: {e}")
            
            conn.commit()
            logging.info(f"Successfully saved optimization {optimization_id}")
            
            return optimization_id
        except Exception as e:
            # Log and handle the error
            logging.error(f"Error saving optimization: {e}")
            if conn:
                conn.rollback()
            # Don't raise, just return None to indicate failure
            return None
        finally:
            if conn:
                conn.close()
    
    def get_optimizations(self, limit=10):
        """Get recent optimizations from the database.
        
        Args:
            limit (int, optional): Maximum number of optimizations to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization data.
        """
        logger.info(f"Fetching {limit} recent optimizations")
        
        with self.connection_pool.get_connection() as conn:
            try:
                query = f"""
                    SELECT id, timestamp, description, num_suppliers 
                    FROM optimizations 
                    ORDER BY timestamp DESC 
                    LIMIT {limit}
                """
                df = pd.read_sql_query(query, conn)
                logger.info(f"Retrieved {len(df)} optimizations")
                return df
            except Exception as e:
                logger.error(f"Error getting optimizations: {e}")
                raise e
    
    def get_optimization_results(self, optimization_id):
        """Get results for a specific optimization.
        
        Args:
            optimization_id (int): ID of the optimization.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization results.
        """
        logger.info(f"Fetching results for optimization {optimization_id}")
        
        with self.connection_pool.get_connection() as conn:
            try:
                query = f"""
                    SELECT s.name, s.cost, s.co2, s.delivery_time, s.ethical_score, r.score as predicted_score, r.selected
                    FROM optimization_results r
                    JOIN suppliers s ON r.supplier_id = s.id
                    WHERE r.optimization_id = {optimization_id}
                    ORDER BY r.score DESC
                """
                df = pd.read_sql_query(query, conn)
                logger.info(f"Retrieved {len(df)} results")
                return df
            except Exception as e:
                logger.error(f"Error getting optimization results: {e}")
                raise e
    
    def get_optimization_trends(self, limit=7):
        """Get optimization trends for the last N optimizations.
        
        Args:
            limit (int, optional): Maximum number of optimizations to include. Defaults to 7.
            
        Returns:
            pandas.DataFrame: DataFrame containing trend data.
        """
        logger.info(f"Fetching optimization trends for last {limit} optimizations")
        
        with self.connection_pool.get_connection() as conn:
            try:
                query = f"""
                    SELECT o.timestamp, 
                           AVG(CASE WHEN r.selected = 1 THEN s.cost ELSE NULL END) as avg_cost,
                           AVG(CASE WHEN r.selected = 1 THEN s.co2 ELSE NULL END) as avg_co2,
                           AVG(CASE WHEN r.selected = 1 THEN s.delivery_time ELSE NULL END) as avg_delivery,
                           AVG(CASE WHEN r.selected = 1 THEN s.ethical_score ELSE NULL END) as avg_ethical
                    FROM optimizations o
                    JOIN optimization_results r ON o.id = r.optimization_id
                    JOIN suppliers s ON r.supplier_id = s.id
                    GROUP BY o.id
                    ORDER BY o.timestamp DESC
                    LIMIT {limit}
                """
                df = pd.read_sql_query(query, conn)
                
                # Reverse the order to have chronological order
                if not df.empty:
                    df = df.iloc[::-1].reset_index(drop=True)
                
                logger.info(f"Retrieved trends for {len(df)} optimizations")
                return df
            except Exception as e:
                logger.error(f"Error getting optimization trends: {e}")
                raise e
    
    def log_activity(self, activity_type, description, details=None):
        """Log an activity to the database.
        
        Args:
            activity_type (str): Type of activity (e.g., 'input', 'optimize', 'export').
            description (str): Description of the activity.
            details (str, optional): Additional details about the activity.
        """
        logger.info(f"Logging activity: {activity_type} - {description}")
        
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Start transaction
                cursor.execute("BEGIN")
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cursor.execute('''
                    INSERT INTO activities (timestamp, activity_type, description, details)
                    VALUES (?, ?, ?, ?)
                ''', (timestamp, activity_type, description, details))
                
                # Commit transaction
                conn.commit()
                logger.info("Activity logged successfully")
            except Exception as e:
                # Rollback transaction on error
                conn.rollback()
                logger.error(f"Error logging activity: {e}")
                raise e
            finally:
                cursor.close()
    
    def get_recent_activities(self, limit=10):
        """Get recent activities from the database.
        
        Args:
            limit (int, optional): Maximum number of activities to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing activity data.
        """
        logger.info(f"Fetching {limit} recent activities")
        
        with self.connection_pool.get_connection() as conn:
            try:
                query = f"""
                    SELECT id, timestamp, activity_type, description, details
                    FROM activities
                    ORDER BY timestamp DESC
                    LIMIT {limit}
                """
                df = pd.read_sql_query(query, conn)
                logger.info(f"Retrieved {len(df)} activities")
                return df
            except Exception as e:
                logger.error(f"Error getting recent activities: {e}")
                raise e

if __name__ == "__main__":
    # Test the database functionality
    
    # Generate sample data
    suppliers = []
    for i in range(1, 16):
        supplier = {
            'name': f"Supplier_{i:04d}",
            'cost': np.random.uniform(100, 1000),
            'co2': np.random.uniform(100, 500),
            'delivery_time': np.random.uniform(1, 30),
            'ethical_score': np.random.uniform(0, 100),
            'predicted_score': np.random.uniform(0, 100)
        }
        suppliers.append(supplier)
    
    df = pd.DataFrame(suppliers)
    
    # Initialize database
    db = Database()
    
    # Save optimization
    optimization_id = db.save_optimization(df, "Test optimization")
    
    # Get optimizations
    optimizations = db.get_optimizations()
    print("Recent optimizations:")
    print(optimizations)
    
    # Get optimization results
    results = db.get_optimization_results(optimization_id)
    print("\nOptimization results:")
    print(results) 