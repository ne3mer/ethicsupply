#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QStatusBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

from .dashboard_page import DashboardPage
from .input_page import InputPage
from .results_page import ResultsPage
from .settings_page import SettingsPage
from .about_page import AboutPage
from .sidebar import Sidebar

class MainWindow(QMainWindow):
    """Main window of the application."""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Ethical AI Supply Chain Optimizer")
        self.setMinimumSize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create pages
        self.dashboard_page = DashboardPage(self)
        self.input_page = InputPage(self)
        self.results_page = ResultsPage(self)
        self.settings_page = SettingsPage(self)
        self.about_page = AboutPage(self)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.results_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.about_page)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #F8F9FA;
                color: #6C757D;
                padding: 5px;
            }
        """)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F9FA;
            }
        """)
    
    def navigate_to(self, index):
        """Navigate to the page at the given index.
        
        Args:
            index (int): Index of the page to navigate to.
        """
        self.stacked_widget.setCurrentIndex(index)
        self.sidebar.set_active_button(index)
    
    def show_status_message(self, message, timeout=5000):
        """Show a message in the status bar.
        
        Args:
            message (str): Message to display.
            timeout (int): Time in milliseconds before the message disappears.
        """
        self.status_bar.showMessage(message, timeout) 