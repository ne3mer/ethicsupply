#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EthicSupply - Ethical AI Supply Chain Optimizer
Run this script to start the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    """Main entry point for the application."""
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