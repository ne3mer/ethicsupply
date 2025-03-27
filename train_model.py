#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EthicSupply - Train and save the TensorFlow model for supplier ranking.
Run this script to train and save the model before running the application.
"""

import os
import sys
import numpy as np
from src.models.supplier_model import SupplierOptimizer, generate_synthetic_data

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Train the supplier optimization model."""
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Generate synthetic training data
    print("Generating synthetic training data...")
    X_train, y_train = generate_synthetic_data(n_samples=1000)
    
    # Create and train model
    print("Creating and training model...")
    model = SupplierOptimizer()
    model.train(X_train, y_train, epochs=100, batch_size=32)
    
    # Save model
    model_path = 'models/supplier_optimizer.h5'
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Test model with sample data
    print("\nTesting model with sample data...")
    sample_suppliers = [
        {
            'name': 'Supplier_01',
            'cost': 300,
            'delivery_time': 3,
            'co2': 100,
            'ethical_score': 75
        },
        {
            'name': 'Supplier_02',
            'cost': 250,
            'delivery_time': 4,
            'co2': 120,
            'ethical_score': 85
        },
        {
            'name': 'Supplier_03',
            'cost': 350,
            'delivery_time': 2,
            'co2': 90,
            'ethical_score': 60
        },
        {
            'name': 'Supplier_04',
            'cost': 280,
            'delivery_time': 5,
            'co2': 150,
            'ethical_score': 45  # Below threshold
        },
        {
            'name': 'Supplier_05',
            'cost': 320,
            'delivery_time': 3,
            'co2': 110,
            'ethical_score': 80
        }
    ]
    
    # Get optimized selection
    selected_indices = model.optimize_suppliers(sample_suppliers)
    
    # Print results
    print("\nSelected suppliers:")
    for idx in selected_indices:
        supplier = sample_suppliers[idx]
        print(f"- {supplier['name']}:")
        print(f"  Cost: ${supplier['cost']}")
        print(f"  Delivery Time: {supplier['delivery_time']} days")
        print(f"  CO2: {supplier['co2']} kg")
        print(f"  Ethical Score: {supplier['ethical_score']}/100")

if __name__ == '__main__':
    main() 