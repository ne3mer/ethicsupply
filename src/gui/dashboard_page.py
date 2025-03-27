#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QScrollArea, QSizePolicy, QGridLayout, QMainWindow
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView

class DashboardPage(QWidget):
    """Dashboard page with performance overview and recent activity."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Add page title
        self.title_label = QLabel("Performance Overview")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
        """)
        self.layout.addWidget(self.title_label)
        
        # Create performance charts
        self.create_performance_charts()
        
        # Create quick actions section
        self.create_quick_actions()
        
        # Create recent activity section
        self.create_recent_activity()
        
        # Add spacer at the bottom
        self.layout.addStretch()
    
    def create_performance_charts(self):
        """Create performance charts section."""
        # Create frame for charts
        chart_frame = QFrame()
        chart_frame.setFrameShape(QFrame.Shape.StyledPanel)
        chart_frame.setFrameShadow(QFrame.Shadow.Raised)
        chart_frame.setStyleSheet("""
            background-color: white;
            border: 1px solid #DEE2E6;
            border-radius: 8px;
        """)
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create section title
        section_title = QLabel("Optimization Trends")
        section_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
        """)
        chart_layout.addWidget(section_title)
        
        # Create web view for Plotly chart
        chart_view = QWebEngineView()
        chart_view.setMinimumHeight(300)
        chart_layout.addWidget(chart_view)
        
        # Create and set chart
        self.create_trend_chart(chart_view)
        
        # Add chart frame to layout
        self.layout.addWidget(chart_frame)
    
    def create_trend_chart(self, web_view):
        """Create and set a trend chart in the web view.
        
        Args:
            web_view (QWebEngineView): The web view to display the chart in.
        """
        # Generate sample data for last 7 days
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        
        # Sample data for costs, CO2, and ethical scores
        costs = [random.uniform(400, 800) for _ in range(7)]
        co2 = [random.uniform(200, 400) for _ in range(7)]
        ethical = [random.uniform(60, 90) for _ in range(7)]
        
        # Create subplot figure
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces
        fig.add_trace(
            go.Scatter(x=dates, y=costs, name="Average Cost ($)", line=dict(color="#007BFF", width=3)),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=dates, y=co2, name="Average CO2 (kg)", line=dict(color="#28A745", width=3)),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=dates, y=ethical, name="Average Ethical Score", line=dict(color="#6610F2", width=3)),
            secondary_y=True,
        )
        
        # Set titles and layout
        fig.update_layout(
            title_text="",
            plot_bgcolor="white",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=50, r=50, t=30, b=80),
        )
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Cost ($) / CO2 (kg)", secondary_y=False)
        fig.update_yaxes(title_text="Ethical Score", secondary_y=True)
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        web_view.setHtml(html)
    
    def create_quick_actions(self):
        """Create quick actions section."""
        # Create frame for quick actions
        action_frame = QFrame()
        action_frame.setFrameShape(QFrame.Shape.StyledPanel)
        action_frame.setFrameShadow(QFrame.Shadow.Raised)
        action_frame.setStyleSheet("""
            background-color: white;
            border: 1px solid #DEE2E6;
            border-radius: 8px;
        """)
        action_layout = QVBoxLayout(action_frame)
        action_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create section title
        section_title = QLabel("Quick Actions")
        section_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
        """)
        action_layout.addWidget(section_title)
        
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Create buttons
        new_opt_btn = QPushButton("Start New Optimization")
        new_opt_btn.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #0056B3;
            }
        """)
        new_opt_btn.clicked.connect(self.start_new_optimization)
        
        load_data_btn = QPushButton("Load Existing Data")
        load_data_btn.setStyleSheet("""
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
        load_data_btn.clicked.connect(self.load_existing_data)
        
        sample_data_btn = QPushButton("Load Sample Data")
        sample_data_btn.setStyleSheet("""
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
        sample_data_btn.clicked.connect(self.load_sample_data)
        
        # Add buttons to layout
        button_layout.addWidget(new_opt_btn)
        button_layout.addWidget(load_data_btn)
        button_layout.addWidget(sample_data_btn)
        button_layout.addStretch()
        
        # Add button layout to action layout
        action_layout.addLayout(button_layout)
        
        # Add action frame to main layout
        self.layout.addWidget(action_frame)
    
    def create_recent_activity(self):
        """Create recent activity section."""
        # Create frame for recent activity
        activity_frame = QFrame()
        activity_frame.setFrameShape(QFrame.Shape.StyledPanel)
        activity_frame.setFrameShadow(QFrame.Shadow.Raised)
        activity_frame.setStyleSheet("""
            background-color: white;
            border: 1px solid #DEE2E6;
            border-radius: 8px;
        """)
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create section title
        section_title = QLabel("Recent Activity")
        section_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
        """)
        activity_layout.addWidget(section_title)
        
        # Create scroll area for activity items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)
        
        # Create activity container
        activity_container = QWidget()
        activity_container_layout = QVBoxLayout(activity_container)
        activity_container_layout.setContentsMargins(0, 0, 0, 0)
        activity_container_layout.setSpacing(10)
        
        # Generate sample activity items
        for i in range(5):
            # Calculate random date and time
            days_ago = random.randint(0, 14)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # Create activity item
            activity_item = self.create_activity_item(
                f"Optimization #{5-i}",
                f"Optimized supply chain with {random.randint(3, 10)} suppliers.",
                timestamp.strftime("%Y-%m-%d %H:%M")
            )
            
            # Add item to container layout
            activity_container_layout.addWidget(activity_item)
        
        # Add container to scroll area
        scroll_area.setWidget(activity_container)
        
        # Set fixed height for scroll area
        scroll_area.setFixedHeight(250)
        
        # Add scroll area to activity layout
        activity_layout.addWidget(scroll_area)
        
        # Add activity frame to main layout
        self.layout.addWidget(activity_frame)
    
    def create_activity_item(self, title, description, timestamp):
        """Create an activity item widget.
        
        Args:
            title (str): Title of the activity.
            description (str): Description of the activity.
            timestamp (str): Timestamp of the activity.
            
        Returns:
            QFrame: The activity item widget.
        """
        # Create item frame
        item_frame = QFrame()
        item_frame.setFrameShape(QFrame.Shape.StyledPanel)
        item_frame.setStyleSheet("""
            background-color: #F8F9FA;
            border: 1px solid #E9ECEF;
            border-radius: 8px;
        """)
        
        # Create item layout
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create item content layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        # Create title label
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #212529;
        """)
        
        # Create description label
        description_label = QLabel(description)
        description_label.setStyleSheet("""
            font-size: 14px;
            color: #6C757D;
        """)
        
        # Create timestamp label
        timestamp_label = QLabel(timestamp)
        timestamp_label.setStyleSheet("""
            font-size: 12px;
            color: #6C757D;
        """)
        
        # Add labels to content layout
        content_layout.addWidget(title_label)
        content_layout.addWidget(description_label)
        content_layout.addWidget(timestamp_label)
        
        # Add content layout to item layout
        item_layout.addLayout(content_layout, stretch=1)
        
        # Create view button
        view_btn = QPushButton("View")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #007BFF;
                border: 1px solid #007BFF;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_activity(title))
        
        # Add view button to item layout
        item_layout.addWidget(view_btn)
        
        return item_frame
    
    def get_main_window(self):
        """Get the main window from the parent widgets.
        
        Returns:
            QMainWindow: The main window.
        """
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent
    
    def start_new_optimization(self):
        """Start a new optimization process."""
        # Navigate to results page through main window
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(1)
    
    def load_existing_data(self):
        """Load existing data from a file."""
        # TODO: Implement file loading dialog
        pass
    
    def load_sample_data(self):
        """Load sample data and navigate to results page."""
        # Navigate to results page through main window
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(1)
    
    def view_activity(self, activity_id):
        """View details of an activity.
        
        Args:
            activity_id (str): ID of the activity to view.
        """
        # Navigate to results page through main window
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to(1) 