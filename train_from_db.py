#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EthicSupply - Train Model from Database
This script trains the TensorFlow model using data from the database.
Run this script to update the model based on historical optimization data.
"""

import os
import sys

def main():
    """Main entry point for the database training script."""
    print("EthicSupply - Training model from database")
    print("==========================================")
    
    try:
        # Import the database model training module
        from src.models.db_model_training import main as train_main
        
        # Run the training
        train_main()
        
        print("\nTraining completed successfully.")
    except ImportError:
        print("Error: Could not import the database model training module.")
        print("Make sure src/models/db_model_training.py exists.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during training: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 