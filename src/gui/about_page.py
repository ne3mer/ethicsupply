#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AboutPage(QWidget):
    """About page with thesis information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Add page title
        title_label = QLabel("About")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
        """)
        self.layout.addWidget(title_label)
        
        # Create about frame
        about_frame = QFrame()
        about_frame.setFrameShape(QFrame.Shape.StyledPanel)
        about_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        about_layout = QVBoxLayout(about_frame)
        about_layout.setSpacing(15)
        
        # Add thesis information
        thesis_title = QLabel("Ethical AI for Optimizing Sustainable Supply Chains in Corporate Decision-Making")
        thesis_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
        """)
        thesis_title.setWordWrap(True)
        about_layout.addWidget(thesis_title)
        
        # Add author information
        author_info = QLabel("Author: Mohammad Afsharfar")
        author_info.setStyleSheet("font-size: 14px; color: #6C757D;")
        about_layout.addWidget(author_info)
        
        # Add supervisor information
        supervisor_info = QLabel("Supervisor: Dr. Alpár Vera Noémi")
        supervisor_info.setStyleSheet("font-size: 14px; color: #6C757D;")
        about_layout.addWidget(supervisor_info)
        
        # Add timeline
        timeline_info = QLabel("Timeline: 2020-2025")
        timeline_info.setStyleSheet("font-size: 14px; color: #6C757D;")
        about_layout.addWidget(timeline_info)
        
        # Add description
        description = QTextEdit()
        description.setReadOnly(True)
        description.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
                font-size: 14px;
                color: #212529;
            }
        """)
        description.setText(
            "This application is part of an MBA thesis focusing on the application of "
            "ethical AI in supply chain optimization. The tool helps corporate decision-makers "
            "optimize their supply chain decisions by balancing efficiency, sustainability, "
            "and fairness.\n\n"
            "Key features:\n"
            "• ML-powered supplier selection\n"
            "• Ethical constraints and fairness metrics\n"
            "• Sustainability optimization\n"
            "• Cost and delivery time efficiency\n\n"
            "The application focuses on grocery retail supply chains (Sainsbury's and Walmart) "
            "and uses a TensorFlow-based neural network to process supplier data and generate "
            "optimized selections."
        )
        about_layout.addWidget(description)
        
        # Add about frame to main layout
        self.layout.addWidget(about_frame)
        
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Create back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #007BFF;
                border: 1px solid #007BFF;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        back_btn.clicked.connect(self.back_to_dashboard)
        
        # Add button to layout
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Add button layout to main layout
        self.layout.addLayout(button_layout)
    
    def get_main_window(self):
        """Get the main window from the parent widgets.
        
        Returns:
            QMainWindow: The main window.
        """
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent
    
    def back_to_dashboard(self):
        """Navigate back to the dashboard."""
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(0) 