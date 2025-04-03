#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

class SupplierModel:
    """TensorFlow model for supplier ranking."""
    
    def __init__(self, model_path=None):
        """Initialize the supplier model.
        
        Args:
            model_path (str, optional): Path to a saved model. If provided, 
                the model will be loaded from this path. Defaults to None.
        """
        self.model = None
        self.is_trained = False
        
        # Load model if path is provided
        if model_path is not None and os.path.exists(model_path):
            self.load_model(model_path)
    
    def build_model(self):
        """Build a new model for supplier ranking."""
        # Create a sequential model
        model = Sequential([
            # Input layer (4 features)
            Dense(32, activation='relu', input_shape=(4,)),
            Dropout(0.2),
            
            # Hidden layers
            Dense(16, activation='relu'),
            Dropout(0.2),
            
            # Output layer (score between 0 and 1)
            Dense(1, activation='linear')
        ])
        
        # Compile the model
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def train(self, X, y, epochs=50, batch_size=8, validation_split=0.2):
        """Train the model on the provided data.
        
        Args:
            X (numpy.ndarray): Input features (cost, CO2, delivery time, ethical score).
            y (numpy.ndarray): Target values (scores).
            epochs (int, optional): Number of epochs to train for. Defaults to 50.
            batch_size (int, optional): Batch size for training. Defaults to 8.
            validation_split (float, optional): Fraction of data to use for validation. 
                Defaults to 0.2.
                
        Returns:
            tensorflow.keras.callbacks.History: Training history.
        """
        # Build model if it doesn't exist
        if self.model is None:
            self.build_model()
        
        # Early stopping callback
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        # Train the model
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stopping],
            verbose=1
        )
        
        self.is_trained = True
        return history
    
    def predict(self, X):
        """Predict scores for the provided features.
        
        Args:
            X (numpy.ndarray): Input features (cost, CO2, delivery time, ethical score).
            
        Returns:
            numpy.ndarray: Predicted scores (between 0 and 1).
            
        Raises:
            ValueError: If the model is not trained.
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model is not trained. Call train() first.")
        
        # Make predictions
        predictions = self.model.predict(X)
        
        # Scale predictions to 0-100 range
        predictions = predictions * 100
        
        # Clip predictions to 0-100 range
        predictions = np.clip(predictions, 0, 100)
        
        return predictions
    
    def save_model(self, path):
        """Save the model to the specified path.
        
        Args:
            path (str): Path to save the model to.
            
        Raises:
            ValueError: If the model is not trained.
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model is not trained. Call train() first.")
        
        self.model.save(path)
    
    def load_model(self, path):
        """Load a model from the specified path.
        
        Args:
            path (str): Path to load the model from.
            
        Raises:
            FileNotFoundError: If the model file doesn't exist.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file {path} not found.")
        
        self.model = load_model(path)
        self.is_trained = True

class SupplierOptimizer:
    """TensorFlow model for optimizing supplier selection."""
    
    def __init__(self):
        """Initialize the model."""
        self.model = self._build_model()
        self.scaler = MinMaxScaler()
    
    def _build_model(self):
        """Build the neural network model.
        
        Returns:
            tf.keras.Model: The built model.
        """
        # Input layer
        inputs = tf.keras.Input(shape=(4,))  # cost, delivery_time, co2, ethical_score
        
        # Hidden layers
        x = tf.keras.layers.Dense(128, activation='relu')(inputs)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Dense(64, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        
        # Output layer (binary classification for each supplier)
        outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
        
        # Create model
        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        
        # Compile model with custom loss function
        model.compile(
            optimizer='adam',
            loss=self._custom_loss,
            metrics=['accuracy']
        )
        
        return model
    
    def _custom_loss(self, y_true, y_pred):
        """Custom loss function that balances efficiency, sustainability, and fairness.
        
        Args:
            y_true (tf.Tensor): True values.
            y_pred (tf.Tensor): Predicted values.
            
        Returns:
            tf.Tensor: Loss value.
        """
        # Efficiency weight (cost and delivery time)
        efficiency_weight = 0.4
        
        # Sustainability weight (CO2 emissions)
        sustainability_weight = 0.3
        
        # Fairness weight (ethical score)
        fairness_weight = 0.3
        
        # Binary cross-entropy loss
        bce_loss = tf.keras.losses.binary_crossentropy(y_true, y_pred)
        
        # Apply weights to different components
        weighted_loss = (
            efficiency_weight * bce_loss +
            sustainability_weight * bce_loss +
            fairness_weight * bce_loss
        )
        
        return weighted_loss
    
    def preprocess_data(self, suppliers_data):
        """Preprocess the supplier data.
        
        Args:
            suppliers_data (list): List of supplier dictionaries.
            
        Returns:
            np.ndarray: Preprocessed data.
        """
        # Convert to DataFrame
        df = pd.DataFrame(suppliers_data)
        
        # Select features for model input
        features = ['cost', 'delivery_time', 'co2', 'ethical_score']
        X = df[features].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled
    
    def optimize_suppliers(self, suppliers_data):
        """Optimize supplier selection.
        
        Args:
            suppliers_data (list): List of supplier dictionaries.
            
        Returns:
            list: List of selected suppliers (indices).
        """
        # Preprocess data
        X = self.preprocess_data(suppliers_data)
        
        # Get predictions
        predictions = self.model.predict(X)
        
        # Scale predictions to 0-100 range for consistency
        predictions = predictions * 100
        predictions = np.clip(predictions, 0, 100)
        
        # Apply ethical constraint (exclude suppliers with ethical score < 50)
        valid_indices = [
            i for i, supplier in enumerate(suppliers_data)
            if supplier['ethical_score'] >= 50
        ]
        
        if not valid_indices:
            return []
        
        # Get predictions for valid suppliers
        valid_predictions = predictions[valid_indices]
        
        # Select top suppliers (highest prediction scores)
        num_suppliers = min(3, len(valid_indices))  # Select up to 3 suppliers
        top_indices = np.argsort(valid_predictions.flatten())[-num_suppliers:][::-1]
        
        # Convert back to original indices
        selected_indices = [valid_indices[i] for i in top_indices]
        
        return selected_indices
    
    def train(self, X_train, y_train, epochs=100, batch_size=32):
        """Train the model.
        
        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training labels.
            epochs (int): Number of training epochs.
            batch_size (int): Batch size for training.
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model.fit(
            X_scaled,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
    
    def save(self, filepath):
        """Save the model.
        
        Args:
            filepath (str): Path to save the model.
        """
        self.model.save(filepath)
    
    def load(self, filepath):
        """Load the model.
        
        Args:
            filepath (str): Path to load the model from.
        """
        self.model = tf.keras.models.load_model(
            filepath,
            custom_objects={'custom_loss': self._custom_loss}
        )

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic data for training the model.
    
    Args:
        n_samples (int, optional): Number of samples to generate. Defaults to 1000.
        
    Returns:
        tuple: X (features) and y (targets) arrays.
    """
    # Generate random features
    cost = np.random.uniform(0, 1, n_samples)
    co2 = np.random.uniform(0, 1, n_samples)
    delivery = np.random.uniform(0, 1, n_samples)
    ethical = np.random.uniform(0, 1, n_samples)
    
    # Calculate target scores based on a weighted sum (plus some noise)
    weights = [0.3, 0.2, 0.2, 0.3]  # cost, CO2, delivery, ethical
    y = (
        weights[0] * cost +
        weights[1] * co2 +
        weights[2] * delivery +
        weights[3] * ethical +
        np.random.normal(0, 0.05, n_samples)  # Add noise
    )
    
    # Clip targets to 0-1 range
    y = np.clip(y, 0, 1)
    
    # Stack features into X
    X = np.column_stack((cost, co2, delivery, ethical))
    
    return X, y

def train_and_save_model(save_path):
    """Train a model on synthetic data and save it.
    
    Args:
        save_path (str): Path to save the model to.
        
    Returns:
        SupplierModel: The trained model.
    """
    # Generate synthetic data
    X, y = generate_synthetic_data(n_samples=1000)
    
    # Create and train the model
    model = SupplierModel()
    model.build_model()
    model.train(X, y, epochs=50)
    
    # Save the model
    model.save_model(save_path)
    
    return model

def normalize_supplier_data(df):
    """Normalize supplier data for model input.
    
    Args:
        df (pandas.DataFrame): DataFrame containing supplier data.
        
    Returns:
        numpy.ndarray: Normalized features.
    """
    # Create a copy of the DataFrame
    normalized_df = df.copy()
    
    # Normalize cost, CO2, and delivery time (0-1 scale, where 0 is worst)
    for col in ['cost', 'co2', 'delivery_time']:
        min_val = normalized_df[col].min()
        max_val = normalized_df[col].max()
        normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
        
        # Invert the values (lower cost, CO2, and delivery time is better)
        normalized_df[col] = 1 - normalized_df[col]
    
    # Normalize ethical score (0-1 scale, where 1 is best)
    normalized_df['ethical_score'] = normalized_df['ethical_score'] / 100
    
    # Extract features
    X = normalized_df[['cost', 'co2', 'delivery_time', 'ethical_score']].values
    
    return X

if __name__ == "__main__":
    # Generate some sample suppliers
    suppliers = []
    for i in range(1, 16):
        supplier = {
            'name': f"Supplier_{i:04d}",
            'cost': np.random.uniform(100, 1000),
            'co2': np.random.uniform(100, 500),
            'delivery_time': np.random.uniform(1, 30),
            'ethical_score': np.random.uniform(0, 100)
        }
        suppliers.append(supplier)
    
    # Create DataFrame
    df = pd.DataFrame(suppliers)
    
    # Normalize features for model input
    X = normalize_supplier_data(df)
    
    # Make sure model directory exists
    os.makedirs("src/models", exist_ok=True)
    
    # Train and save the model
    model = train_and_save_model("src/models/supplier_model.h5")
    
    # Make predictions
    predictions = model.predict(X)
    
    # Add predictions to DataFrame
    df['predicted_score'] = predictions
    
    # Sort by predicted score (descending)
    df = df.sort_values('predicted_score', ascending=False).reset_index(drop=True)
    
    # Print results
    print("Top 5 suppliers:")
    print(df[['name', 'cost', 'co2', 'delivery_time', 'ethical_score', 'predicted_score']].head(5)) 