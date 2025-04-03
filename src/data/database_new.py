#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import pandas as pd
from datetime import datetime
import threading
import time
import logging

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
    
    def __new__(cls, db_path='ethicsupply_new.db'):
        """Singleton pattern to ensure only one database instance exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.db_path = os.path.join(os.path.dirname(__file__), db_path)
                cls._instance.connection_lock = threading.Lock()
                cls._instance._setup_database()
            return cls._instance
    
    def __init__(self, db_path='ethicsupply_new.db'):
        """Initialize the database.
        
        Args:
            db_path (str, optional): Path to the database file. 
                Defaults to 'ethicsupply_new.db'.
        """
        pass  # Initialization is done in __new__
    
    def _setup_database(self):
        """Set up the database and create tables."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Create tables
        conn = sqlite3.connect(self.db_path, timeout=60.0)
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
            conn.close()
    
    def _get_connection(self):
        """Get a connection to the database.
        
        Returns:
            sqlite3.Connection: A connection to the database.
        """
        # Set timeout to 60 seconds to handle busy database
        conn = sqlite3.connect(self.db_path, timeout=60.0)
        
        # Configure connection
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=60000")
        cursor.close()
        
        return conn
    
    def save_suppliers(self, suppliers_df):
        """Save suppliers to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data.
            
        Returns:
            list: List of supplier IDs.
        """
        logger.info(f"Saving {len(suppliers_df)} suppliers")
        
        conn = self._get_connection()
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
            conn.close()
    
    def get_suppliers(self):
        """Get all suppliers from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing supplier data.
        """
        logger.info("Fetching all suppliers")
        
        conn = self._get_connection()
        try:
            query = "SELECT id, name, cost, co2, delivery_time, ethical_score FROM suppliers"
            df = pd.read_sql_query(query, conn)
            logger.info(f"Retrieved {len(df)} suppliers")
            return df
        finally:
            conn.close()
    
    def save_optimization(self, suppliers_df, description=None):
        """Save an optimization run to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data with scores.
            description (str, optional): Description of the optimization. Defaults to None.
            
        Returns:
            int: ID of the optimization.
        """
        logger.info(f"Saving optimization with {len(suppliers_df)} suppliers")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Start transaction
            cursor.execute("BEGIN")
            
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
            logger.error(f"Error saving optimization: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def get_optimizations(self, limit=10):
        """Get recent optimizations from the database.
        
        Args:
            limit (int, optional): Maximum number of optimizations to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization data.
        """
        logger.info(f"Fetching {limit} recent optimizations")
        
        conn = self._get_connection()
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
        finally:
            conn.close()
    
    def get_optimization_results(self, optimization_id):
        """Get results for a specific optimization.
        
        Args:
            optimization_id (int): ID of the optimization.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization results.
        """
        logger.info(f"Fetching results for optimization {optimization_id}")
        
        conn = self._get_connection()
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
        finally:
            conn.close()
    
    def get_optimization_trends(self, limit=7):
        """Get optimization trends for the last N optimizations.
        
        Args:
            limit (int, optional): Maximum number of optimizations to include. Defaults to 7.
            
        Returns:
            pandas.DataFrame: DataFrame containing trend data.
        """
        logger.info(f"Fetching optimization trends for last {limit} optimizations")
        
        conn = self._get_connection()
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
        finally:
            conn.close()
    
    def log_activity(self, activity_type, description, details=None):
        """Log an activity to the database.
        
        Args:
            activity_type (str): Type of activity (e.g., 'input', 'optimize', 'export').
            description (str): Description of the activity.
            details (str, optional): Additional details about the activity.
        """
        logger.info(f"Logging activity: {activity_type} - {description}")
        
        conn = self._get_connection()
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
            conn.close()
    
    def get_recent_activities(self, limit=10):
        """Get recent activities from the database.
        
        Args:
            limit (int, optional): Maximum number of activities to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing activity data.
        """
        logger.info(f"Fetching {limit} recent activities")
        
        conn = self._get_connection()
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
        finally:
            conn.close()

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