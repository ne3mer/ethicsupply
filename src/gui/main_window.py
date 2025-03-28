#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QSizePolicy, QStatusBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

from .dashboard_page import DashboardPage
from .input_page import InputPage
from .results_page import ResultsPage
from .settings_page import SettingsPage
from .about_page import AboutPage
from .recent_activity_page import RecentActivityPage
from .sidebar import Sidebar

class MainWindow(QMainWindow):
    """Main window of the application."""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("EthicSupply")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        layout.addWidget(self.sidebar)
        
        # Create content area
        self.content_area = QWidget()
        self.content_area.setLayout(QVBoxLayout())
        self.content_area.layout().setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.content_area)
        
        # Create pages
        self.pages = {
            'dashboard': DashboardPage(self),
            'input': InputPage(self),
            'results': ResultsPage(self),
            'recent_activity': RecentActivityPage(self),
            'settings': SettingsPage(self),
            'about': AboutPage(self)
        }
        
        # Add pages to content area
        for page in self.pages.values():
            self.content_area.layout().addWidget(page)
            page.hide()
        
        # Set up status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Show dashboard by default
        self.navigate_to('dashboard')
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F9FA;
            }
        """)
    
    def navigate_to(self, page_name):
        """Navigate to the specified page."""
        if page_name in self.pages:
            # Hide all pages
            for page in self.pages.values():
                page.hide()
            
            # Show selected page
            self.pages[page_name].show()
            
            # Update status bar
            status_messages = {
                'dashboard': "Dashboard - View key metrics and start new optimizations",
                'input': "Input - Add or modify supplier data",
                'results': "Results - View optimization results and supplier comparisons",
                'recent_activity': "Recent Activity - View recent actions and history",
                'settings': "Settings - Configure application preferences",
                'about': "About - Learn more about EthicSupply"
            }
            self.statusBar.showMessage(status_messages.get(page_name, "Ready"))
    
    def show_status_message(self, message, timeout=5000):
        """Show a message in the status bar.
        
        Args:
            message (str): Message to display.
            timeout (int): Time in milliseconds before the message disappears.
        """
        self.statusBar.showMessage(message, timeout) 