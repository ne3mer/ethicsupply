#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import pandas as pd
from datetime import datetime
import threading
import time
import contextlib
import logging
import traceback

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('EthicSupply.Database')

class Database:
    """SQLite database for storing supplier data and optimization history."""
    
    _instance = None
    _lock = threading.Lock()
    _connection_count = 0
    
    def __new__(cls, db_path='src/data/ethicsupply.db'):
        """Singleton pattern to ensure only one database instance exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.db_path = db_path
                cls._instance.connection_lock = threading.Lock()
                cls._instance._setup_database()
            return cls._instance
    
    def __init__(self, db_path='src/data/ethicsupply.db'):
        """Initialize the database.
        
        Args:
            db_path (str, optional): Path to the database file. 
                Defaults to 'src/data/ethicsupply.db'.
        """
        pass  # Initialization is done in __new__
    
    def _setup_database(self):
        """Set up the database and create tables."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Remove any existing WAL files
        try:
            wal_file = f"{self.db_path}-wal"
            shm_file = f"{self.db_path}-shm"
            if os.path.exists(wal_file):
                os.remove(wal_file)
            if os.path.exists(shm_file):
                os.remove(shm_file)
            logger.info("Removed existing WAL files")
        except Exception as e:
            logger.warning(f"Failed to remove WAL files: {e}")
        
        # Create tables
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
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
    
    @contextlib.contextmanager
    def _get_connection(self):
        """Get a connection to the database with retry logic.
        
        Yields:
            sqlite3.Connection: A connection to the database.
        """
        max_retries = 10
        retry_delay = 0.5  # seconds
        last_error = None
        conn = None
        
        # Track connection count
        with self._lock:
            self._connection_count += 1
            current_count = self._connection_count
        
        logger.debug(f"Getting connection (count: {current_count})")
        
        for attempt in range(max_retries):
            try:
                # Set timeout to 60 seconds to handle busy database
                conn = sqlite3.connect(self.db_path, timeout=60.0, isolation_level='EXCLUSIVE')
                logger.debug(f"Connection established on attempt {attempt + 1}")
                
                cursor = conn.cursor()
                
                # Configure connection
                pragmas = [
                    ("journal_mode", "WAL"),
                    ("busy_timeout", 60000),
                    ("foreign_keys", "ON"),
                    ("synchronous", "NORMAL"),
                    ("locking_mode", "EXCLUSIVE")
                ]
                
                for pragma, value in pragmas:
                    cursor.execute(f"PRAGMA {pragma}={value}")
                    result = cursor.execute(f"PRAGMA {pragma}").fetchone()
                    logger.debug(f"Set {pragma} to {value}, got {result[0]}")
                
                yield conn
                
                # Commit any pending transactions
                if conn.in_transaction:
                    logger.debug("Committing pending transaction")
                    conn.commit()
                
                return
            except sqlite3.OperationalError as e:
                last_error = e
                logger.warning(f"Database error on attempt {attempt + 1}: {e}")
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                logger.error(f"Database error: {e}\n{traceback.format_exc()}")
                raise
            except Exception as e:
                last_error = e
                logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
                raise
            finally:
                if conn:
                    try:
                        conn.close()
                        logger.debug("Connection closed")
                    except Exception as e:
                        logger.warning(f"Error closing connection: {e}")
                
                with self._lock:
                    self._connection_count -= 1
                    logger.debug(f"Connection count decreased to {self._connection_count}")
        
        if last_error:
            raise last_error
    
    def save_suppliers(self, suppliers_df):
        """Save suppliers to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data.
            
        Returns:
            list: List of supplier IDs.
        """
        logger.info(f"Saving {len(suppliers_df)} suppliers")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            supplier_ids = []
            
            try:
                # Start transaction
                cursor.execute("BEGIN EXCLUSIVE")
                logger.debug("Started EXCLUSIVE transaction")
                
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
                logger.error(f"Error saving suppliers: {e}\n{traceback.format_exc()}")
                raise e
    
    def get_suppliers(self):
        """Get all suppliers from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing supplier data.
        """
        logger.info("Fetching all suppliers")
        
        with self._get_connection() as conn:
            query = "SELECT id, name, cost, co2, delivery_time, ethical_score FROM suppliers"
            df = pd.read_sql_query(query, conn)
            logger.info(f"Retrieved {len(df)} suppliers")
            return df
    
    def save_optimization(self, suppliers_df, description=None):
        """Save an optimization run to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data with scores.
            description (str, optional): Description of the optimization. Defaults to None.
            
        Returns:
            int: ID of the optimization.
        """
        logger.info(f"Saving optimization with {len(suppliers_df)} suppliers")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Start transaction
                cursor.execute("BEGIN EXCLUSIVE")
                logger.debug("Started EXCLUSIVE transaction")
                
                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Insert optimization
                cursor.execute('''
                    INSERT INTO optimizations (timestamp, description, num_suppliers)
                    VALUES (?, ?, ?)
                ''', (
                    timestamp,
                    description or f"Optimization run at {timestamp}",
                    len(suppliers_df)
                ))
                
                optimization_id = cursor.lastrowid
                logger.debug(f"Created optimization with ID {optimization_id}")
                
                # Save supplier IDs if they don't exist
                supplier_ids = self.save_suppliers(suppliers_df[['name', 'cost', 'co2', 'delivery_time', 'ethical_score']])
                
                # Insert optimization results
                for i, (_, row) in enumerate(suppliers_df.iterrows()):
                    cursor.execute('''
                        INSERT INTO optimization_results (optimization_id, supplier_id, score, selected)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        optimization_id,
                        supplier_ids[i],
                        row['predicted_score'],
                        1 if i < 3 else 0  # Select top 3 suppliers
                    ))
                
                # Commit transaction
                conn.commit()
                logger.info(f"Successfully saved optimization {optimization_id}")
                return optimization_id
            except Exception as e:
                # Rollback transaction on error
                conn.rollback()
                logger.error(f"Error saving optimization: {e}\n{traceback.format_exc()}")
                raise e
    
    def get_optimizations(self, limit=10):
        """Get recent optimizations from the database.
        
        Args:
            limit (int, optional): Maximum number of optimizations to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization data.
        """
        logger.info(f"Fetching {limit} recent optimizations")
        
        with self._get_connection() as conn:
            query = f"""
                SELECT id, timestamp, description, num_suppliers 
                FROM optimizations 
                ORDER BY timestamp DESC 
                LIMIT {limit}
            """
            df = pd.read_sql_query(query, conn)
            logger.info(f"Retrieved {len(df)} optimizations")
            return df
    
    def get_optimization_results(self, optimization_id):
        """Get results for a specific optimization.
        
        Args:
            optimization_id (int): ID of the optimization.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization results.
        """
        logger.info(f"Fetching results for optimization {optimization_id}")
        
        with self._get_connection() as conn:
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
    
    def get_optimization_trends(self, limit=7):
        """Get optimization trends for the last N optimizations.
        
        Args:
            limit (int, optional): Maximum number of optimizations to include. Defaults to 7.
            
        Returns:
            pandas.DataFrame: DataFrame containing trend data.
        """
        logger.info(f"Fetching optimization trends for last {limit} optimizations")
        
        with self._get_connection() as conn:
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
    
    def log_activity(self, activity_type, description, details=None):
        """Log an activity to the database.
        
        Args:
            activity_type (str): Type of activity (e.g., 'input', 'optimize', 'export').
            description (str): Description of the activity.
            details (str, optional): Additional details about the activity.
        """
        logger.info(f"Logging activity: {activity_type} - {description}")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Start transaction
                cursor.execute("BEGIN EXCLUSIVE")
                logger.debug("Started EXCLUSIVE transaction")
                
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
                logger.error(f"Error logging activity: {e}\n{traceback.format_exc()}")
                raise e
    
    def get_recent_activities(self, limit=10):
        """Get recent activities from the database.
        
        Args:
            limit (int, optional): Maximum number of activities to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing activity data.
        """
        logger.info(f"Fetching {limit} recent activities")
        
        with self._get_connection() as conn:
            query = f"""
                SELECT id, timestamp, activity_type, description, details
                FROM activities
                ORDER BY timestamp DESC
                LIMIT {limit}
            """
            df = pd.read_sql_query(query, conn)
            logger.info(f"Retrieved {len(df)} activities")
            return df

if __name__ == "__main__":
    # Test the database functionality
    import numpy as np
    
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