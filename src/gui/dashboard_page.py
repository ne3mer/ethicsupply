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
        # Get real data from database
        main_window = self.get_main_window()
        if not main_window or not hasattr(main_window, 'db'):
            return
            
        # Get optimization trends from database
        trends_df = main_window.db.get_optimization_trends(limit=7)
        
        if trends_df.empty:
            # Show "No data" message if no optimizations exist
            fig = go.Figure()
            fig.add_annotation(
                text="No optimization data available",
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(
                plot_bgcolor="white",
                margin=dict(l=50, r=50, t=30, b=80),
            )
            html = fig.to_html(include_plotlyjs='cdn')
            web_view.setHtml(html)
            return
        
        # Create subplot figure
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces
        fig.add_trace(
            go.Scatter(
                x=trends_df['timestamp'],
                y=trends_df['avg_cost'],
                name="Average Cost ($)",
                line=dict(color="#007BFF", width=3)
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(
                x=trends_df['timestamp'],
                y=trends_df['avg_co2'],
                name="Average CO2 (kg)",
                line=dict(color="#28A745", width=3)
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(
                x=trends_df['timestamp'],
                y=trends_df['avg_ethical'],
                name="Average Ethical Score",
                line=dict(color="#6610F2", width=3)
            ),
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
        # Navigate to input page through main window
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to('input')
    
    def load_existing_data(self):
        """Load existing data from a file."""
        # TODO: Implement file loading dialog
        pass
    
    def load_sample_data(self):
        """Load sample data and navigate to input page."""
        # Navigate to input page through main window
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to('input')
    
    def create_dashboard_content(self, layout):
        """Create the main dashboard content."""
        # Create grid layout for metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(20)
        
        # Add metric cards
        self.add_metric_card(metrics_grid, 0, 0, "Total Suppliers", "0", "suppliers")
        self.add_metric_card(metrics_grid, 0, 1, "Average Cost", "$0.00", "cost")
        self.add_metric_card(metrics_grid, 0, 2, "Average CO2", "0 kg", "co2")
        self.add_metric_card(metrics_grid, 1, 0, "Average Delivery Time", "0 days", "delivery")
        self.add_metric_card(metrics_grid, 1, 1, "Average Ethical Score", "0/100", "ethical")
        self.add_metric_card(metrics_grid, 1, 2, "Optimization Status", "Not Started", "status")
        
        # Add metrics grid to main layout
        layout.addLayout(metrics_grid)
        
        # Add stretch to push content to the top
        layout.addStretch()
    
    def create_action_buttons(self, layout):
        """Create action buttons for the dashboard."""
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Create buttons
        input_btn = QPushButton("Input Data")
        input_btn.setStyleSheet("""
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
        input_btn.clicked.connect(lambda: self.get_main_window().navigate_to('input'))
        
        results_btn = QPushButton("View Results")
        results_btn.setStyleSheet("""
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
        results_btn.clicked.connect(lambda: self.get_main_window().navigate_to('results'))
        
        # Add buttons to layout
        button_layout.addWidget(input_btn)
        button_layout.addWidget(results_btn)
        button_layout.addStretch()
        
        # Add button layout to main layout
        layout.addLayout(button_layout) 