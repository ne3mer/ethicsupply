#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd
import numpy as np
from src.models.supplier_model import normalize_supplier_data, SupplierModel
import os

def generate_sample_suppliers(num_suppliers=15):
    """Generate sample supplier data.
    
    Args:
        num_suppliers (int, optional): Number of suppliers to generate. Defaults to 15.
        
    Returns:
        pandas.DataFrame: DataFrame containing supplier data.
    """
    suppliers = []
    
    for i in range(1, num_suppliers + 1):
        supplier = {
            'name': f"Supplier_{i:04d}",
            'cost': random.uniform(100, 1000),
            'co2': random.uniform(100, 500),
            'delivery_time': random.uniform(1, 30),
            'ethical_score': random.uniform(0, 100)
        }
        suppliers.append(supplier)
    
    return pd.DataFrame(suppliers)

def rank_suppliers(suppliers_df, model_path='src/models/supplier_model.h5'):
    """Rank suppliers using the TensorFlow model.
    
    Args:
        suppliers_df (pandas.DataFrame): DataFrame containing supplier data.
        model_path (str, optional): Path to the saved model. 
            Defaults to 'src/models/supplier_model.h5'.
            
    Returns:
        pandas.DataFrame: DataFrame with predicted scores added.
    """
    # Create a copy of the DataFrame
    df = suppliers_df.copy()
    
    # Normalize features for model input
    X = normalize_supplier_data(df)
    
    # Check if model exists
    if not os.path.exists(model_path):
        # Use simplified ranking without TensorFlow
        return simplified_ranking(df)
    
    # Load the model
    try:
        model = SupplierModel(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return simplified_ranking(df)
    
    # Make predictions
    predictions = model.predict(X)
    
    # Add predicted scores to DataFrame
    df['predicted_score'] = predictions
    
    # Sort by predicted score (descending)
    df = df.sort_values('predicted_score', ascending=False).reset_index(drop=True)
    
    return df

def simplified_ranking(suppliers_df):
    """Simplified ranking without using TensorFlow.
    
    Args:
        suppliers_df (pandas.DataFrame): DataFrame containing supplier data.
        
    Returns:
        pandas.DataFrame: DataFrame with predicted scores added.
    """
    # Create a copy of the DataFrame
    df = suppliers_df.copy()
    
    # Normalize features
    normalized_df = df.copy()
    for col in ['cost', 'co2', 'delivery_time']:
        min_val = normalized_df[col].min()
        max_val = normalized_df[col].max()
        normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
    
    # Invert cost, CO2, and delivery time (lower is better)
    for col in ['cost', 'co2', 'delivery_time']:
        normalized_df[col] = 1 - normalized_df[col]
    
    # Normalize ethical score
    normalized_df['ethical_score'] = normalized_df['ethical_score'] / 100
    
    # Calculate predicted scores
    weights = {
        'cost': 0.3,
        'co2': 0.2,
        'delivery_time': 0.2,
        'ethical_score': 0.3
    }
    
    predicted_scores = (
        normalized_df['cost'] * weights['cost'] +
        normalized_df['co2'] * weights['co2'] +
        normalized_df['delivery_time'] * weights['delivery_time'] +
        normalized_df['ethical_score'] * weights['ethical_score']
    ) * 100
    
    # Add some random noise to the scores
    noise = np.random.normal(0, 5, len(predicted_scores))
    predicted_scores = predicted_scores + noise
    
    # Clip scores to 0-100 range
    predicted_scores = np.clip(predicted_scores, 0, 100)
    
    # Add predicted scores to DataFrame
    df['predicted_score'] = predicted_scores
    
    # Sort by predicted score (descending)
    df = df.sort_values('predicted_score', ascending=False).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Test the sample data generation
    suppliers_df = generate_sample_suppliers()
    ranked_df = rank_suppliers(suppliers_df)
    
    print("Sample suppliers:")
    print(ranked_df[['name', 'cost', 'co2', 'delivery_time', 'ethical_score', 'predicted_score']].head(5)) 