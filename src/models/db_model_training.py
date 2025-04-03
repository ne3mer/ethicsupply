#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EthicSupply - Database to ML Model Connection
This module connects the database with the TensorFlow model for continuous learning.
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Add parent directory to the path to correctly import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.database_pool import Database
from src.models.supplier_model import SupplierModel, SupplierOptimizer, normalize_supplier_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('EthicSupply.ModelTraining')

class DatabaseModelTrainer:
    """Connects the database to the TensorFlow model for continuous learning."""
    
    def __init__(self, model_path=None):
        """Initialize the trainer.
        
        Args:
            model_path (str, optional): Path to a saved model. 
                If None, a new model will be created. Defaults to None.
        """
        # Initialize database connection
        self.db = Database()
        
        # Initialize the model
        self.supplier_model = SupplierModel(model_path)
        if self.supplier_model.model is None:
            logger.info("Building new model")
            self.supplier_model.build_model()
        else:
            logger.info(f"Loaded existing model from {model_path}")
    
    def get_training_data_from_db(self, limit=None):
        """Get training data from the database.
        
        Args:
            limit (int, optional): Maximum number of optimization results to include.
                If None, all data will be included. Defaults to None.
        
        Returns:
            tuple: X (features) and y (targets) arrays for training.
        """
        logger.info("Retrieving optimization data from database")
        
        # Get recent optimizations
        optimizations = self.db.get_optimizations(limit=limit if limit else 100)
        
        if optimizations.empty:
            logger.warning("No optimization data found in the database")
            return None, None
        
        # Initialize lists for features and targets
        features = []
        targets = []
        
        # Process each optimization
        for _, optimization in optimizations.iterrows():
            optimization_id = optimization['id']
            
            # Get optimization results
            results = self.db.get_optimization_results(optimization_id)
            
            if results.empty:
                continue
            
            # Extract features from results
            for _, result in results.iterrows():
                # Extract features
                supplier_features = [
                    result['cost'],
                    result['co2'],
                    result['delivery_time'],
                    result['ethical_score']
                ]
                
                # Extract target (was this supplier selected?)
                target = result['selected']
                
                features.append(supplier_features)
                targets.append(target)
        
        if not features:
            logger.warning("No valid training data found")
            return None, None
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(targets)
        
        logger.info(f"Retrieved {len(X)} training samples from database")
        
        return X, y
    
    def train_model_with_db_data(self, epochs=50, batch_size=32, validation_split=0.2):
        """Train the model with data from the database.
        
        Args:
            epochs (int, optional): Number of training epochs. Defaults to 50.
            batch_size (int, optional): Batch size for training. Defaults to 32.
            validation_split (float, optional): Fraction of data to use for validation.
                Defaults to 0.2.
                
        Returns:
            bool: True if training was successful, False otherwise.
        """
        # Get training data from database
        X, y = self.get_training_data_from_db()
        
        if X is None or y is None:
            logger.warning("No training data available")
            return False
        
        # Normalize the features
        X_normalized = self._normalize_features(X)
        
        # Train the model
        logger.info(f"Training model with {len(X)} samples")
        try:
            history = self.supplier_model.train(
                X_normalized, 
                y, 
                epochs=epochs, 
                batch_size=batch_size, 
                validation_split=validation_split
            )
            
            logger.info("Model training completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
    
    def _normalize_features(self, X):
        """Normalize features for model input.
        
        Args:
            X (numpy.ndarray): Raw features.
            
        Returns:
            numpy.ndarray: Normalized features.
        """
        # Create a DataFrame with the features
        df = pd.DataFrame(X, columns=['cost', 'co2', 'delivery_time', 'ethical_score'])
        
        # Normalize the features
        X_normalized = normalize_supplier_data(df)
        
        return X_normalized
    
    def save_model(self, path='models/supplier_model_from_db.h5'):
        """Save the trained model.
        
        Args:
            path (str, optional): Path to save the model to.
                Defaults to 'models/supplier_model_from_db.h5'.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the model
        try:
            self.supplier_model.save_model(path)
            logger.info(f"Model saved to {path}")
            
            # Log the activity in the database
            self.db.log_activity(
                activity_type="model",
                description="Trained and saved model from database data",
                details=f"Model saved to {path}"
            )
            
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def incremental_learning(self, path='models/supplier_model_from_db.h5', interval_hours=24):
        """Set up incremental learning from database data.
        
        Args:
            path (str, optional): Path to save the model to.
                Defaults to 'models/supplier_model_from_db.h5'.
            interval_hours (int, optional): Number of hours between training.
                Defaults to 24.
        """
        # Train the model with current data
        success = self.train_model_with_db_data()
        
        if success:
            # Save the model
            self.save_model(path)
            
            logger.info(f"Incremental learning complete. Model saved to {path}")
            logger.info(f"Next training scheduled in {interval_hours} hours")
            
            # Note: In a production environment, you would set up a scheduler
            # like APScheduler to run this function periodically
            
            return True
        else:
            logger.warning("Incremental learning failed due to lack of data or training error")
            return False


def main():
    """Main entry point for the database-to-model training."""
    # Define the model path
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'supplier_model_from_db.h5')
    
    # Check if the model already exists
    if os.path.exists(model_path):
        print(f"Loading existing model from {model_path}")
    else:
        print("No existing model found. Will create a new one.")
    
    # Initialize the trainer
    trainer = DatabaseModelTrainer(model_path if os.path.exists(model_path) else None)
    
    # Train the model with database data
    print("Training model with database data...")
    success = trainer.train_model_with_db_data()
    
    if success:
        # Save the model
        print("Training successful. Saving model...")
        trainer.save_model(model_path)
        print(f"Model saved to {model_path}")
    else:
        print("Training failed due to lack of data or training error.")
        print("Generating synthetic data for initial training...")
        
        # If no data in the database, use synthetic data for initial training
        from src.models.supplier_model import generate_synthetic_data
        
        X, y = generate_synthetic_data(n_samples=1000)
        
        print(f"Training model with {len(X)} synthetic samples...")
        trainer.supplier_model.train(X, y, epochs=50)
        
        # Save the model
        trainer.supplier_model.save_model(model_path)
        print(f"Model trained with synthetic data and saved to {model_path}")
    
    print("\nModel is now ready for use in the application.")
    print("You can run this script periodically to continue training the model with new data.")


if __name__ == "__main__":
    main() 