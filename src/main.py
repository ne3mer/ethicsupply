#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDir

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import application components
from src.gui.main_window import MainWindow

def main():
    """Initialize and run the EthicSupply application."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("EthicSupply")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set default font
    default_font = QFont("Inter", 10)
    app.setFont(default_font)
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 