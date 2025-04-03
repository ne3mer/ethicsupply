#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EthicSupply - Ethical AI Supply Chain Optimizer
Run this script to start the application.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    """Main entry point for the application."""
    # Check if a database-trained model exists and use it
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    db_model_path = os.path.join(model_dir, 'supplier_model_from_db.h5')
    
    # If the database-trained model doesn't exist, try to train it first
    if not os.path.exists(db_model_path) and os.path.isfile(os.path.join('src', 'models', 'db_model_training.py')):
        try:
            print("No database-trained model found. Trying to train model from database data...")
            from src.models.db_model_training import main as train_main
            train_main()
        except Exception as e:
            print(f"Error training model from database: {e}")
            print("Will use default model instead.")
    
    # Create the application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 