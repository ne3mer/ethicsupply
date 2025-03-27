#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpacerItem, QSizePolicy, QMainWindow
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor

class SidebarButton(QPushButton):
    """Custom button for the sidebar."""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        # Set button properties
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 10px;
                text-align: left;
                border-radius: 0px;
                font-size: 14px;
                color: #212529;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
            QPushButton:checked {
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
        """)
        self.setCheckable(True)

class Sidebar(QWidget):
    """Sidebar navigation for the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set widget properties
        self.setObjectName("sidebar")
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #DEE2E6;
            }
        """)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create header
        self.create_header()
        
        # Create navigation buttons
        self.create_nav_buttons()
        
        # Add spacer at the bottom
        self.layout.addSpacerItem(QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        ))
    
    def create_header(self):
        """Create the header section of the sidebar."""
        # Create header widget
        header_widget = QWidget()
        header_widget.setFixedHeight(100)
        header_widget.setStyleSheet("""
            background-color: #007BFF;
            padding: 10px;
        """)
        
        # Create header layout
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 15, 15, 15)
        header_layout.setSpacing(5)
        
        # Create title label
        title_label = QLabel("EthicSupply")
        title_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        # Create subtitle label
        subtitle_label = QLabel("AI Supply Chain Optimizer")
        subtitle_label.setStyleSheet("""
            color: white;
            font-size: 12px;
        """)
        
        # Add labels to header layout
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Add header to sidebar layout
        self.layout.addWidget(header_widget)
    
    def create_nav_buttons(self):
        """Create the navigation buttons for the sidebar."""
        # Create buttons
        self.dashboard_btn = SidebarButton("Dashboard")
        self.input_data_btn = SidebarButton("Input Data")
        self.results_btn = SidebarButton("Results")
        self.settings_btn = SidebarButton("Settings")
        
        # Add buttons to layout
        self.layout.addWidget(self.dashboard_btn)
        self.layout.addWidget(self.input_data_btn)
        self.layout.addWidget(self.results_btn)
        self.layout.addWidget(self.settings_btn)
        
        # Connect signals to slots
        self.dashboard_btn.clicked.connect(lambda: self.navigate_to(0))  # Dashboard page
        self.input_data_btn.clicked.connect(lambda: self.navigate_to(1))  # Input page
        self.results_btn.clicked.connect(lambda: self.navigate_to(2))  # Results page
        self.settings_btn.clicked.connect(lambda: self.navigate_to(3))  # Settings/About page
        
        # Set default active button
        self.dashboard_btn.setChecked(True)
    
    def get_main_window(self):
        """Get the main window from the parent widgets.
        
        Returns:
            QMainWindow: The main window.
        """
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent
    
    def navigate_to(self, index):
        """Navigate to the page corresponding to the given index.
        
        Args:
            index (int): Index of the page to navigate to.
        """
        # Get the main window and navigate
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(index)
    
    def set_active_button(self, index):
        """Set the active button based on the current page index.
        
        Args:
            index (int): Index of the current page.
        """
        # Reset all buttons
        self.dashboard_btn.setChecked(False)
        self.input_data_btn.setChecked(False)
        self.results_btn.setChecked(False)
        self.settings_btn.setChecked(False)
        
        # Set the active button
        if index == 0:
            self.dashboard_btn.setChecked(True)
        elif index == 1:
            self.input_data_btn.setChecked(True)
        elif index == 2:
            self.results_btn.setChecked(True)
        elif index == 3:
            self.settings_btn.setChecked(True) 