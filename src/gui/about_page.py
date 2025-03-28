#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AboutPage(QWidget):
    """About page showing application information and credits."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def get_main_window(self):
        """Get the main window from the parent widgets."""
        from PyQt6.QtWidgets import QMainWindow
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent
    
    def setup_ui(self):
        """Set up the about page UI."""
        # Create main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        
        # Title
        title = QLabel("About EthicSupply")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)
        
        # Application Information
        app_info = QFrame()
        app_info.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        app_layout = QVBoxLayout(app_info)
        
        app_title = QLabel("Application Information")
        app_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        app_layout.addWidget(app_title)
        
        app_details = QLabel(
            "EthicSupply is an AI-powered supply chain optimization tool that "
            "helps businesses make ethical and sustainable supplier selection decisions. "
            "The application uses advanced machine learning algorithms to analyze "
            "supplier data and provide recommendations based on multiple criteria "
            "including cost, quality, sustainability, and ethical practices."
        )
        app_details.setWordWrap(True)
        app_layout.addWidget(app_details)
        
        content_layout.addWidget(app_info)
        
        # Developer Information
        dev_info = QFrame()
        dev_info.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        dev_layout = QVBoxLayout(dev_info)
        
        dev_title = QLabel("Developer Information")
        dev_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        dev_layout.addWidget(dev_title)
        
        dev_details = QLabel(
            "Name: Mohammad Afsharfar\n"
            "Student ID: IZD6CT\n"
            "Email: ne3mer@gmail.com\n"
            "Department: MBA\n"
            "University: Budapest Metropolitan University Of Budapest"
        )
        dev_layout.addWidget(dev_details)
        
        content_layout.addWidget(dev_info)
        
        # Thesis Information
        thesis_info = QFrame()
        thesis_info.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        thesis_layout = QVBoxLayout(thesis_info)
        
        thesis_title = QLabel("Thesis Information")
        thesis_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        thesis_layout.addWidget(thesis_title)
        
        thesis_details = QLabel(
            "Title: Ethical AI for Optimizing Sustainable Supply Chains in Corporate Decision-Making\n"
            "Supervisor: Alpár Vera Noémi Dr\n"
            "Year: 2025\n\n"
            "This thesis explores the application of artificial intelligence and "
            "machine learning techniques in supply chain optimization, with a "
            "particular focus on ethical considerations and sustainable practices."
        )
        thesis_details.setWordWrap(True)
        thesis_layout.addWidget(thesis_details)
        
        content_layout.addWidget(thesis_info)
        
        # Version Information
        version_info = QFrame()
        version_info.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        version_layout = QVBoxLayout(version_info)
        
        version_title = QLabel("Version Information")
        version_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        version_layout.addWidget(version_title)
        
        version_details = QLabel(
            "Version: 1.0.0\n"
            "Release Date: March 2025\n"
            "Python Version: 3.8+\n"
            "PyQt Version: 6.4.0\n"
            "TensorFlow Version: 2.12.0"
        )
        version_layout.addWidget(version_details)
        
        content_layout.addWidget(version_info)
        
        # Add content to scroll area
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Back button
        back_button = QPushButton("Back to Dashboard")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056B3;
            }
        """)
        back_button.clicked.connect(lambda: self.get_main_window().navigate_to('dashboard'))
        layout.addWidget(back_button)
        
        self.setLayout(layout) 