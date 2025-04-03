#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QScrollArea, QSizePolicy, QMainWindow
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from datetime import datetime, timedelta
import pandas as pd
from src.data.database_pool import Database

class RecentActivityPage(QWidget):
    """Page to display recent activity in the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize database
        self.db = Database()
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Add page title
        self.title_label = QLabel("Recent Activity")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
        """)
        self.layout.addWidget(self.title_label)
        
        # Create scroll area for activity feed
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CED4DA;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create container widget for activity items
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(15)
        
        # Set container as scroll area widget
        self.scroll.setWidget(self.container)
        
        # Add scroll area to main layout
        self.layout.addWidget(self.scroll)
        
        # Create back button
        self.create_back_button()
        
        # Load initial activities
        self.refresh_activities()
    
    def refresh_activities(self):
        """Refresh the activity feed with latest data from the database."""
        # Clear existing activities
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get recent activities from database
        activities_df = self.db.get_recent_activities(limit=10)
        
        if activities_df.empty:
            # Add "No activities" message
            no_activities_label = QLabel("No recent activities")
            no_activities_label.setStyleSheet("""
                font-size: 14px;
                color: #6C757D;
                font-style: italic;
            """)
            no_activities_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.container_layout.addWidget(no_activities_label)
        else:
            # Add each activity
            for _, activity in activities_df.iterrows():
                # Convert timestamp to relative time
                timestamp = datetime.strptime(activity['timestamp'], "%Y-%m-%d %H:%M:%S")
                time_diff = datetime.now() - timestamp
                
                if time_diff.days > 0:
                    time_text = f"{time_diff.days} day{'s' if time_diff.days != 1 else ''} ago"
                elif time_diff.seconds >= 3600:
                    hours = time_diff.seconds // 3600
                    time_text = f"{hours} hour{'s' if hours != 1 else ''} ago"
                elif time_diff.seconds >= 60:
                    minutes = time_diff.seconds // 60
                    time_text = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
                else:
                    time_text = "Just now"
                
                self.add_activity_item(
                    self.container_layout,
                    activity['description'],
                    time_text,
                    activity['activity_type'],
                    activity['details']
                )
        
        # Add stretch to push items to the top
        self.container_layout.addStretch()
    
    def add_activity_item(self, layout, activity_text, time_text, activity_type, details=None):
        """Add an activity item to the layout.
        
        Args:
            layout (QVBoxLayout): Layout to add the activity item to.
            activity_text (str): Text describing the activity.
            time_text (str): Text showing when the activity occurred.
            activity_type (str): Type of activity for icon and color.
            details (str, optional): Additional details about the activity.
        """
        # Create activity frame
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                padding: 15px;
            }
            QFrame:hover {
                background-color: #F8F9FA;
            }
        """)
        
        # Create frame layout
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(15, 10, 15, 10)
        frame_layout.setSpacing(5)
        
        # Create top row layout
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        # Set icon and color based on activity type
        icon_colors = {
            "input": "#007BFF",  # Blue
            "optimize": "#28A745",  # Green
            "export": "#FFC107",  # Yellow
            "add": "#17A2B8",  # Cyan
            "settings": "#6C757D",  # Gray
            "refresh": "#6C757D",  # Gray
            "update": "#17A2B8",  # Cyan
            "start": "#6C757D"  # Gray
        }
        
        # Create activity icon
        icon_label = QLabel("•")
        icon_label.setStyleSheet(f"""
            color: {icon_colors.get(activity_type, '#6C757D')};
            font-size: 20px;
        """)
        top_layout.addWidget(icon_label)
        
        # Create activity text
        activity_label = QLabel(activity_text)
        activity_label.setStyleSheet("""
            font-size: 14px;
            color: #212529;
        """)
        top_layout.addWidget(activity_label)
        
        # Add stretch to push time to the right
        top_layout.addStretch()
        
        # Create time text
        time_label = QLabel(time_text)
        time_label.setStyleSheet("""
            font-size: 12px;
            color: #6C757D;
        """)
        top_layout.addWidget(time_label)
        
        # Add top layout to frame layout
        frame_layout.addLayout(top_layout)
        
        # Add details if available
        if details:
            details_label = QLabel(details)
            details_label.setStyleSheet("""
                font-size: 12px;
                color: #6C757D;
                margin-left: 25px;
            """)
            details_label.setWordWrap(True)
            frame_layout.addWidget(details_label)
        
        # Add frame to layout
        layout.addWidget(frame)
        
        # Make the entire frame clickable
        frame.mousePressEvent = lambda e: self.handle_activity_click(activity_type, activity_text)
    
    def handle_activity_click(self, activity_type, activity_text):
        """Handle click on an activity item.
        
        Args:
            activity_type (str): Type of activity.
            activity_text (str): Text describing the activity.
        """
        main_window = self.get_main_window()
        if not main_window:
            return
            
        # Navigate based on activity type
        if activity_type in ["input", "add", "update"]:
            # Navigate to input page
            main_window.navigate_to(1)
        elif activity_type in ["optimize", "refresh"]:
            # Navigate to results page
            main_window.navigate_to(2)
        elif activity_type == "export":
            # Show export dialog
            self.show_export_dialog()
        elif activity_type == "settings":
            # Navigate to settings page
            main_window.navigate_to(4)
    
    def show_export_dialog(self):
        """Show export dialog for results."""
        # TODO: Implement export dialog
        pass
    
    def create_back_button(self):
        """Create and add the back button to the layout."""
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
    
    def back_to_dashboard(self):
        """Navigate back to the dashboard."""
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(0)
    
    def get_main_window(self):
        """Get the main window from the parent widgets.
        
        Returns:
            QMainWindow: The main window.
        """
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent 