#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import pandas as pd
from datetime import datetime

class Database:
    """SQLite database for storing supplier data and optimization history."""
    
    def __init__(self, db_path='src/data/ethicsupply.db'):
        """Initialize the database.
        
        Args:
            db_path (str, optional): Path to the database file. 
                Defaults to 'src/data/ethicsupply.db'.
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self):
        """Get a connection to the database.
        
        Returns:
            sqlite3.Connection: A connection to the database.
        """
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()
    
    def save_suppliers(self, suppliers_df):
        """Save suppliers to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data.
            
        Returns:
            list: List of supplier IDs.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        supplier_ids = []
        
        # Insert each supplier
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
        
        conn.commit()
        conn.close()
        
        return supplier_ids
    
    def get_suppliers(self):
        """Get all suppliers from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing supplier data.
        """
        conn = self.get_connection()
        query = "SELECT id, name, cost, co2, delivery_time, ethical_score FROM suppliers"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def save_optimization(self, suppliers_df, description=None):
        """Save an optimization run to the database.
        
        Args:
            suppliers_df (pandas.DataFrame): DataFrame containing supplier data with scores.
            description (str, optional): Description of the optimization. Defaults to None.
            
        Returns:
            int: ID of the optimization.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()
        
        return optimization_id
    
    def get_optimizations(self, limit=10):
        """Get recent optimizations from the database.
        
        Args:
            limit (int, optional): Maximum number of optimizations to return. Defaults to 10.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization data.
        """
        conn = self.get_connection()
        query = f"""
            SELECT id, timestamp, description, num_suppliers 
            FROM optimizations 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_optimization_results(self, optimization_id):
        """Get results for a specific optimization.
        
        Args:
            optimization_id (int): ID of the optimization.
            
        Returns:
            pandas.DataFrame: DataFrame containing optimization results.
        """
        conn = self.get_connection()
        query = f"""
            SELECT s.name, s.cost, s.co2, s.delivery_time, s.ethical_score, r.score as predicted_score, r.selected
            FROM optimization_results r
            JOIN suppliers s ON r.supplier_id = s.id
            WHERE r.optimization_id = {optimization_id}
            ORDER BY r.score DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_optimization_trends(self, limit=7):
        """Get optimization trends for the last N optimizations.
        
        Args:
            limit (int, optional): Maximum number of optimizations to include. Defaults to 7.
            
        Returns:
            pandas.DataFrame: DataFrame containing trend data.
        """
        conn = self.get_connection()
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
        conn.close()
        
        # Reverse the order to have chronological order
        df = df.iloc[::-1].reset_index(drop=True)
        
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