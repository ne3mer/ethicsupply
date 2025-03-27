#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpacerItem, QSizePolicy, QMainWindow, QFrame
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

class Sidebar(QFrame):
    """Sidebar widget with navigation buttons."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set frame properties
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #DEE2E6;
            }
        """)
        self.setFixedWidth(250)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        
        # Add logo/title
        title = QLabel("EthicSupply")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
            margin-bottom: 20px;
        """)
        self.layout.addWidget(title)
        
        # Create navigation buttons
        self.nav_buttons = []
        
        # Dashboard button
        dashboard_btn = self.create_nav_button("Dashboard", 0)
        dashboard_btn.setChecked(True)  # Set as default selected
        self.layout.addWidget(dashboard_btn)
        
        # Input button
        input_btn = self.create_nav_button("Input Data", 1)
        self.layout.addWidget(input_btn)
        
        # Results button
        results_btn = self.create_nav_button("Results", 2)
        self.layout.addWidget(results_btn)
        
        # Recent Activity button
        activity_btn = self.create_nav_button("Recent Activity", 3)
        self.layout.addWidget(activity_btn)
        
        # Settings button
        settings_btn = self.create_nav_button("Settings", 4)
        self.layout.addWidget(settings_btn)
        
        # Add stretch to push buttons to the top
        self.layout.addStretch()
    
    def create_nav_button(self, text, index):
        """Create a navigation button.
        
        Args:
            text (str): Button text.
            index (int): Page index to navigate to.
            
        Returns:
            QPushButton: The created navigation button.
        """
        button = QPushButton(text)
        button.setCheckable(True)
        button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 12px 15px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                color: #6C757D;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
                color: #007BFF;
            }
            QPushButton:checked {
                background-color: #E3F2FD;
                color: #007BFF;
                font-weight: bold;
            }
        """)
        button.clicked.connect(lambda: self.navigate_to(index))
        self.nav_buttons.append(button)
        return button
    
    def set_active_button(self, index):
        """Set the active navigation button.
        
        Args:
            index (int): Index of the button to set as active.
        """
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
    
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
        """Navigate to the specified page.
        
        Args:
            index (int): Index of the page to navigate to.
        """
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(index)
            self.set_active_button(index) 