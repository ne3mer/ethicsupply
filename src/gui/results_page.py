#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.spatial.distance import pdist, squareform
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QFileDialog, QMainWindow, QScrollArea, QSpinBox, QComboBox, QLineEdit, QTextBrowser
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QBrush
from PyQt6.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
import os
import json
import csv
import math
import traceback

class ResultsPage(QWidget):
    """Results page with supplier rankings and optimization details."""
    
    def __init__(self, parent=None):
        """Initialize the results page.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        # Initialize variables
        self.df = None
        self.tabs = None
        self.parent_window = parent
        
        # Setup UI
        self.setup_ui()
        
        # Only generate sample data if no suppliers exist yet
        try:
            if self.df is None or len(self.df) == 0:
                self.initialize_with_sample_data()
        except Exception as e:
            print(f"Error initializing with sample data: {e}")
            # Initialize with empty DataFrame to prevent further errors
            self.df = pd.DataFrame(columns=['name', 'cost', 'co2', 'delivery_time', 'predicted_score'])
    
    def setup_ui(self):
        """Set up the UI components for the results page."""
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Create action buttons
        self.create_action_buttons()
        
        # Create tabs container
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 15px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
        """)
        
        # Add tabs widget to main layout
        self.layout.addWidget(self.tabs)
        
        # Set up the tab content
        self.setup_tabs()
    
    def setup_tabs(self):
        """Set up the tabs for the results page."""
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-bottom-color: transparent;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 15px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
        """)
        
        # Create Supplier Table tab
        rankings_tab = QWidget()
        rankings_layout = QVBoxLayout(rankings_tab)
        rankings_layout.setContentsMargins(0, 0, 0, 0)
        rankings_layout.setSpacing(0)
        self.create_supplier_table(rankings_layout)
        
        # Create Performance Chart tab
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        performance_layout.setContentsMargins(0, 0, 0, 0)
        performance_layout.setSpacing(0)
        self.create_supplier_ranking_chart(performance_layout)
        
        # Create AI Explanation tab
        explanation_tab = QWidget()
        explanation_layout = QVBoxLayout(explanation_tab)
        explanation_layout.setContentsMargins(0, 0, 0, 0)
        explanation_layout.setSpacing(0)
        self.create_explanation_content(explanation_layout)
        
        # Create Trade-off Analysis tab
        tradeoff_tab = QWidget()
        tradeoff_layout = QVBoxLayout(tradeoff_tab)
        tradeoff_layout.setContentsMargins(0, 0, 0, 0)
        tradeoff_layout.setSpacing(0)
        self.create_tradeoff_chart(tradeoff_layout)
        
        # Create Supplier Network tab
        network_tab = QWidget()
        network_layout = QVBoxLayout(network_tab)
        network_layout.setContentsMargins(0, 0, 0, 0)
        network_layout.setSpacing(0)
        self.create_supplier_network(network_layout)
        
        # Create Top 3 Comparison tab
        comparison_tab = QWidget()
        comparison_layout = QVBoxLayout(comparison_tab)
        comparison_layout.setContentsMargins(0, 0, 0, 0)
        comparison_layout.setSpacing(0)
        
        # Add radar chart title
        radar_title = QLabel("Top 3 Suppliers Comparison")
        radar_title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        comparison_layout.addWidget(radar_title)
        
        self.create_radar_chart(comparison_layout)
        
        # Add tabs to tab widget
        self.tabs.addTab(rankings_tab, "Supplier Rankings")
        self.tabs.addTab(performance_tab, "Performance Chart")
        self.tabs.addTab(explanation_tab, "AI Explanation")
        self.tabs.addTab(tradeoff_tab, "Trade-off Analysis")
        self.tabs.addTab(network_tab, "Supplier Network")
        self.tabs.addTab(comparison_tab, "Top 3 Comparison")
        
        # Add tab widget to main layout
        self.layout.addWidget(self.tabs)
    
    def create_supplier_ranking_chart(self, layout):
        """Create a bar chart of supplier rankings.
        
        Args:
            layout (QVBoxLayout): Layout to add the chart to.
        """
        # Create title
        title = QLabel("Supplier Performance Rankings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Create chart frame
        web_view = QWebEngineView()
        web_view.setMinimumHeight(500)
        
        # Create the chart
        fig = go.Figure()
        
        # Add bars for each supplier
        if self.df is not None and len(self.df) > 0:
            suppliers = self.df['name'].tolist()
            scores = self.df['predicted_score'].tolist()
            
            # Sort by score in descending order
            sorted_data = sorted(zip(suppliers, scores), key=lambda x: x[1], reverse=True)
            suppliers, scores = zip(*sorted_data) if sorted_data else ([], [])
            
            # Create bar chart
            fig.add_trace(go.Bar(
                x=suppliers,
                y=scores,
                text=[f"{score:.1f}" for score in scores],
                textposition='auto',
                marker_color=['#4CAF50' if i < 3 else '#2196F3' for i in range(len(suppliers))],
                hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
            ))
            
            # Update layout
            fig.update_layout(
                title={
                    'text': 'Supplier Performance Scores',
                    'font': {'size': 24}
                },
                xaxis_title='Supplier',
                yaxis_title='Performance Score (0-100)',
                yaxis_range=[0, 100],
                height=500,
                margin=dict(l=50, r=50, t=80, b=80),
                plot_bgcolor='white',
            )
            
            # Add horizontal line for average score
            avg_score = sum(scores) / len(scores) if scores else 0
            fig.add_shape(type="line",
                x0=-0.5, y0=avg_score, x1=len(suppliers)-0.5, y1=avg_score,
                line=dict(color="red", width=2, dash="dash")
            )
            
            # Add annotation for average score
            fig.add_annotation(
                x=len(suppliers)/2,
                y=avg_score + 5,
                text=f"Average Score: {avg_score:.1f}",
                showarrow=False,
                font=dict(color="red")
            )
        else:
            # Display a message when no data is available
            fig.add_annotation(
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                text="No supplier data available. Please add suppliers in the Input page.",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=500,
                plot_bgcolor='white',
            )
        
        # Convert to HTML
        chart_html = fig.to_html(include_plotlyjs='cdn')
        
        # Display in web view
        web_view.setHtml(chart_html)
        layout.addWidget(web_view)
    
    def create_tradeoff_chart(self, layout):
        """Create a scatter plot showing cost vs. CO2 tradeoff.
        
        Args:
            layout (QVBoxLayout): Layout to add the chart to.
        """
        # Create title
        title = QLabel("Cost vs. CO2 Emissions Trade-off")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Create chart frame
        web_view = QWebEngineView()
        web_view.setMinimumHeight(500)
        
        # Create the chart
        fig = go.Figure()
        
        if self.df is not None and len(self.df) > 0:
            # Add scatter points for each supplier
            suppliers = self.df['name'].tolist()
            costs = self.df['cost'].tolist()
            co2 = self.df['co2'].tolist()
            scores = self.df['predicted_score'].tolist()
            
            # Determine size based on performance score (larger = better score)
            sizes = [max(score, 20) for score in scores]
            
            # Create scatter plot
            fig.add_trace(go.Scatter(
                x=costs,
                y=co2,
                mode='markers+text',
                marker=dict(
                    size=sizes,
                    color=scores,
                    colorscale='Viridis',
                    colorbar=dict(title='Score'),
                    showscale=True,
                    line=dict(width=1, color='black')
                ),
                text=suppliers,
                textposition='top center',
                hovertemplate='<b>%{text}</b><br>Cost: $%{x:.2f}<br>CO2: %{y:.1f} kg<br>Score: %{marker.color:.1f}<extra></extra>'
            ))
            
            # Update layout
            fig.update_layout(
                title={
                    'text': 'Cost vs. CO2 Emissions Trade-off',
                    'font': {'size': 24}
                },
                xaxis_title='Cost ($)',
                yaxis_title='CO2 Emissions (kg)',
                height=500,
                margin=dict(l=50, r=50, t=80, b=80),
                plot_bgcolor='white',
            )
            
            # Add quadrant lines using the median values
            median_cost = self.df['cost'].median()
            median_co2 = self.df['co2'].median()
            
            # Vertical line at median cost
            fig.add_shape(type="line",
                x0=median_cost, y0=min(co2), x1=median_cost, y1=max(co2),
                line=dict(color="gray", width=1, dash="dot")
            )
            
            # Horizontal line at median CO2
            fig.add_shape(type="line",
                x0=min(costs), y0=median_co2, x1=max(costs), y1=median_co2,
                line=dict(color="gray", width=1, dash="dot")
            )
            
            # Add annotations for quadrants
            fig.add_annotation(
                x=min(costs) + (median_cost - min(costs))/2,
                y=min(co2) + (median_co2 - min(co2))/2,
                text="Low Cost,<br>Low CO2",
                showarrow=False,
                font=dict(color="green", size=12),
                bgcolor="rgba(0,255,0,0.1)",
                bordercolor="green",
                borderwidth=1,
                borderpad=4
            )
            
            fig.add_annotation(
                x=median_cost + (max(costs) - median_cost)/2,
                y=min(co2) + (median_co2 - min(co2))/2,
                text="High Cost,<br>Low CO2",
                showarrow=False,
                font=dict(color="orange", size=12),
                bgcolor="rgba(255,165,0,0.1)",
                bordercolor="orange",
                borderwidth=1,
                borderpad=4
            )
            
            fig.add_annotation(
                x=min(costs) + (median_cost - min(costs))/2,
                y=median_co2 + (max(co2) - median_co2)/2,
                text="Low Cost,<br>High CO2",
                showarrow=False,
                font=dict(color="orange", size=12),
                bgcolor="rgba(255,165,0,0.1)",
                bordercolor="orange",
                borderwidth=1,
                borderpad=4
            )
            
            fig.add_annotation(
                x=median_cost + (max(costs) - median_cost)/2,
                y=median_co2 + (max(co2) - median_co2)/2,
                text="High Cost,<br>High CO2",
                showarrow=False,
                font=dict(color="red", size=12),
                bgcolor="rgba(255,0,0,0.1)",
                bordercolor="red",
                borderwidth=1,
                borderpad=4
            )
        else:
            # Display a message when no data is available
            fig.add_annotation(
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                text="No supplier data available. Please add suppliers in the Input page.",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=500,
                plot_bgcolor='white',
            )
        
        # Convert to HTML
        chart_html = fig.to_html(include_plotlyjs='cdn')
        
        # Display in web view
        web_view.setHtml(chart_html)
        layout.addWidget(web_view)
    
    def create_radar_chart(self, layout):
        """Create a radar chart comparing top 3 suppliers.
        
        Args:
            layout (QVBoxLayout): Layout to add the chart to.
        """
        # Create chart frame
        web_view = QWebEngineView()
        web_view.setMinimumHeight(500)
        
        # Create radar chart
        fig = go.Figure()
        
        if self.df is not None and len(self.df) > 0:
            # Get top 3 suppliers
            top_suppliers = self.df.head(3)
            
            # Define radar chart categories and values
            categories = ['Cost Efficiency', 'CO2 Efficiency', 'Delivery Efficiency', 'Ethical Score', 'Overall Score']
            
            # For each supplier, calculate normalized scores
            for i, (_, supplier) in enumerate(top_suppliers.iterrows()):
                # Normalize values for radar chart (0-1 scale where 1 is best)
                cost_norm = 1 - ((supplier['cost'] - self.df['cost'].min()) / (self.df['cost'].max() - self.df['cost'].min()) if self.df['cost'].max() != self.df['cost'].min() else 0.5)
                co2_norm = 1 - ((supplier['co2'] - self.df['co2'].min()) / (self.df['co2'].max() - self.df['co2'].min()) if self.df['co2'].max() != self.df['co2'].min() else 0.5)
                delivery_norm = 1 - ((supplier['delivery_time'] - self.df['delivery_time'].min()) / (self.df['delivery_time'].max() - self.df['delivery_time'].min()) if self.df['delivery_time'].max() != self.df['delivery_time'].min() else 0.5)
                
                # Ensure ethical_score exists
                if 'ethical_score' not in supplier:
                    ethical_norm = 0.7  # Default value if not present
                else:
                    ethical_norm = supplier['ethical_score'] / 100  # Normalize 0-100 to 0-1
                
                overall_norm = supplier['predicted_score'] / 100  # Normalize 0-100 to 0-1
                
                # Values for radar chart (must close the loop)
                values = [cost_norm * 100, co2_norm * 100, delivery_norm * 100, ethical_norm * 100, overall_norm * 100]
                
                # Add trace for this supplier
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=supplier['name'],
                    hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'
                ))
            
            # Update layout
            fig.update_layout(
                title={
                    'text': 'Top 3 Suppliers Comparison',
                    'font': {'size': 24}
                },
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                height=500,
                margin=dict(l=80, r=80, t=100, b=80),
                showlegend=True
            )
        else:
            # Display a message when no data is available
            fig.add_annotation(
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                text="No supplier data available. Please add suppliers in the Input page.",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=500,
                plot_bgcolor='white',
            )
        
        # Convert to HTML
        chart_html = fig.to_html(include_plotlyjs='cdn')
        
        # Display in web view
        web_view.setHtml(chart_html)
        layout.addWidget(web_view)
    
    def create_supplier_table(self, layout):
        """Create a table showing supplier details.
        
        Args:
            layout (QVBoxLayout): Layout to add the table to.
        """
        # Create table title
        title = QLabel("Supplier Details")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Create table
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 6px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # Set up columns
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Supplier", "Cost ($)", "CO2 (kg)", "Delivery (days)", "Ethical Score", "AI Score"])
        
        # Set column widths
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 6):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        # Populate table
        self._populate_table()
        
        # Connect selection signal
        self.table.selectionModel().selectionChanged.connect(self._selection_changed)
        
        # Add search widget
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-weight: bold;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter suppliers...")
        self.search_input.textChanged.connect(self._filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Add table to layout
        layout.addWidget(self.table)
        
        # Add detail widget
        self.detail_widget = QLabel("Select a supplier to view details")
        self.detail_widget.setStyleSheet("""
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
        """)
        self.detail_widget.setWordWrap(True)
        layout.addWidget(self.detail_widget)
    
    def _populate_table(self):
        """Populate the supplier table with data."""
        if self.df is not None and len(self.df) > 0:
            # Set table rows
            self.table.setRowCount(len(self.df))
            
            # Add data to table
            for i, (_, row) in enumerate(self.df.iterrows()):
                # Supplier name
                name_item = QTableWidgetItem(row['name'])
                self.table.setItem(i, 0, name_item)
                
                # Cost
                cost_item = QTableWidgetItem(f"{row['cost']:.2f}")
                cost_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 1, cost_item)
                
                # CO2
                co2_item = QTableWidgetItem(f"{row['co2']:.1f}")
                co2_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 2, co2_item)
                
                # Delivery time
                delivery_item = QTableWidgetItem(f"{row['delivery_time']:.1f}")
                delivery_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 3, delivery_item)
                
                # Ethical score - check if it exists in the dataframe
                if 'ethical_score' in row and pd.notna(row['ethical_score']):
                    ethical_item = QTableWidgetItem(f"{row['ethical_score']:.1f}")
                else:
                    # Calculate from normalized metrics
                    normalized_cost = 1 - ((row['cost'] - self.df['cost'].min()) / (self.df['cost'].max() - self.df['cost'].min()) if self.df['cost'].max() > self.df['cost'].min() else 0.5)
                    normalized_co2 = 1 - ((row['co2'] - self.df['co2'].min()) / (self.df['co2'].max() - self.df['co2'].min()) if self.df['co2'].max() > self.df['co2'].min() else 0.5)
                    normalized_delivery = 1 - ((row['delivery_time'] - self.df['delivery_time'].min()) / (self.df['delivery_time'].max() - self.df['delivery_time'].min()) if self.df['delivery_time'].max() > self.df['delivery_time'].min() else 0.5)
                    
                    calculated_ethical = (normalized_cost * 0.3 + normalized_co2 * 0.4 + normalized_delivery * 0.3) * 100
                    ethical_item = QTableWidgetItem(f"{calculated_ethical:.1f}")
                
                ethical_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 4, ethical_item)
                
                # AI Score
                score_item = QTableWidgetItem(f"{row['predicted_score']:.1f}")
                score_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 5, score_item)
                
                # Color-code the top 3 suppliers
                if i < 3:
                    for j in range(6):
                        self.table.item(i, j).setBackground(QColor('#e6f7e6'))  # Light green
        else:
            self.table.setRowCount(0)
    
    def _filter_table(self):
        """Filter the table based on search criteria."""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            match = True
            
            # Check if supplier name matches search text
            supplier_item = self.table.item(row, 0)
            if supplier_item and search_text:
                supplier_name = supplier_item.text().lower()
                if search_text not in supplier_name:
                    match = False
            
            # Show or hide row
            self.table.setRowHidden(row, not match)

    def _selection_changed(self):
        """Handle selection change in the supplier table."""
        selected = self.table.selectedIndexes()
        if selected and self.df is not None and len(self.df) > 0:
            row = selected[0].row()
            if row < len(self.df):
                supplier_name = self.table.item(row, 0).text()
                self.show_supplier_details(supplier_name)
    
    def show_supplier_details(self, supplier_name):
        """Show detailed information for the selected supplier."""
        if self.df is None or len(self.df) == 0:
            return
            
        # Find supplier in DataFrame
        supplier = self.df[self.df['name'] == supplier_name]
        if len(supplier) == 0:
            return
            
        # Get the first matching supplier
        supplier = supplier.iloc[0]
        
        # Create HTML for supplier details
        details = f"""
        <h3>{supplier['name']}</h3>
        <p><b>AI Score:</b> {supplier['predicted_score']:.1f}/100</p>
        <p><b>Cost:</b> ${supplier['cost']:.2f}</p>
        <p><b>CO2 Emissions:</b> {supplier['co2']:.1f} kg</p>
        <p><b>Delivery Time:</b> {supplier['delivery_time']:.1f} days</p>
        """
        
        # Add ethical score if available
        if 'ethical_score' in supplier:
            details += f"<p><b>Ethical Score:</b> {supplier['ethical_score']:.1f}/100</p>"
        
        # Add additional information if available
        additional_fields = ['supplier_id', 'contact_email', 'region', 'sustainability_cert', 
                           'payment_terms', 'production_capacity', 'certifications', 'specialization']
        
        additional_info = ""
        for field in additional_fields:
            if field in supplier and pd.notna(supplier[field]):
                label = ' '.join(word.capitalize() for word in field.split('_'))
                additional_info += f"<p><b>{label}:</b> {supplier[field]}</p>"
        
        if additional_info:
            details += "<h4>Additional Information</h4>" + additional_info
        
        # Update detail widget
        self.detail_widget.setText(details)
        self.detail_widget.setTextFormat(Qt.TextFormat.RichText)
    
    def _export_dialog(self):
        """Handle export dialog."""
        # Implement the logic to show export dialog
        print("Export dialog")
    
    def create_template_file(self, path=None):
        """Create a template CSV file for supplier data.
        
        Args:
            path (str, optional): Path to save the template file to. Defaults to None.
            
        Returns:
            str: Path to the template file.
        """
        # If no path provided, create one in the app directory
        if not path:
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            path = os.path.join(app_dir, 'supplier_export_template.csv')
        
        # Create dataframe with template data
        template_df = pd.DataFrame([
            {
                'name': 'Supplier A (Example)',
                'cost': 500,
                'co2': 75,
                'delivery_time': 14,
                'supplier_id': 'SUP001',
                'contact_email': 'contact@suppliera.com',
                'region': 'North America',
                'sustainability_cert': 'ISO 14001',
                'payment_terms': 'Net 30',
                'production_capacity': '10000 units/month',
                'notes': 'This is an example supplier. Please delete this row before importing.'
            },
            {
                'name': 'Supplier B (Example)',
                'cost': 450,
                'co2': 65,
                'delivery_time': 10,
                'supplier_id': 'SUP002',
                'contact_email': 'contact@supplierb.com',
                'region': 'Europe',
                'sustainability_cert': 'Green Business',
                'payment_terms': 'Net 15',
                'production_capacity': '8000 units/month',
                'notes': 'This is an example supplier. Please delete this row before importing.'
            },
            {
                'name': 'Supplier C (Example)',
                'cost': 600,
                'co2': 45,
                'delivery_time': 21,
                'supplier_id': 'SUP003',
                'contact_email': 'contact@supplierc.com',
                'region': 'Asia',
                'sustainability_cert': 'LEED',
                'payment_terms': 'Net 45',
                'production_capacity': '15000 units/month',
                'notes': 'This is an example supplier. Please delete this row before importing.'
            }
        ])
        
        # Add instructions as CSV comments
        instructions = [
            '# SUPPLIER DATA IMPORT TEMPLATE',
            '# ',
            '# REQUIRED FIELDS:',
            '# - name: Supplier name (required)',
            '# - cost: Cost per unit in USD (required, numeric)',
            '# - co2: CO2 emissions in kg per unit (required, numeric)',
            '# - delivery_time: Delivery time in days (required, numeric)',
            '# ',
            '# OPTIONAL FIELDS:',
            '# - supplier_id: Your internal ID for the supplier',
            '# - contact_email: Primary contact email',
            '# - region: Geographic region of the supplier',
            '# - sustainability_cert: Any sustainability certifications',
            '# - payment_terms: Payment terms (e.g., Net 30)',
            '# - production_capacity: Production capacity (e.g., 10000 units/month)',
            '# - notes: Any additional notes about the supplier',
            '# ',
            '# NOTE: Delete these instructions and the example data rows before importing',
            '# NOTE: The ethical_score will be calculated automatically by the AI model'
        ]
        
        # Write template to file
        try:
            # Write the instructions as comments
            with open(path, 'w') as f:
                for line in instructions:
                    f.write(line + '\n')
            
            # Append the DataFrame without header (since we wrote comments)
            template_df.to_csv(path, mode='a', index=False)
            
            return path
        except Exception as e:
            print(f"Error creating template file: {e}")
            return None
    
    def _get_supplier_analysis(self):
        """Generate detailed analysis of why each top supplier was selected."""
        top_3 = self.df.head(3)
        analysis_parts = []
        
        for i, supplier in top_3.iterrows():
            # Calculate percentile ranks
            cost_rank = (self.df['cost'] >= supplier['cost']).mean() * 100
            co2_rank = (self.df['co2'] >= supplier['co2']).mean() * 100
            delivery_rank = (self.df['delivery_time'] >= supplier['delivery_time']).mean() * 100
            ethical_rank = (self.df['ethical_score'] <= supplier['ethical_score']).mean() * 100
            
            # Generate supplier-specific analysis
            strengths = []
            if cost_rank < 25:
                strengths.append("competitive pricing")
            if co2_rank < 25:
                strengths.append("excellent environmental performance")
            if delivery_rank < 25:
                strengths.append("superior delivery times")
            if ethical_rank < 25:
                strengths.append("outstanding ethical standards")
            
            # Handle case where supplier has no outstanding strengths
            if not strengths:
                strengths_text = "balanced performance across all metrics"
            elif len(strengths) == 1:
                strengths_text = strengths[0]
            else:
                strengths_text = ", ".join(strengths[:-1]) + f" and {strengths[-1]}"
            
            analysis = f"""
            {supplier['name']} (AI Score: {supplier['predicted_score']:.1f}/100):
            • Ranked in the top {cost_rank:.0f}% for cost (${supplier['cost']:.2f})
            • Ranked in the top {co2_rank:.0f}% for CO2 emissions ({supplier['co2']:.1f} kg)
            • Ranked in the top {delivery_rank:.0f}% for delivery time ({supplier['delivery_time']:.1f} days)
            • Ranked in the top {ethical_rank:.0f}% for ethical standards ({supplier['ethical_score']:.1f}/100)
            
            This supplier was selected for its {strengths_text}. The combination of these factors contributes to our balanced optimization approach.
            """
            analysis_parts.append(analysis)
        
        return "\n".join(analysis_parts)
    
    def update_results(self, suppliers_data):
        """Update the results with new supplier data.
        
        Args:
            suppliers_data (list): List of dictionaries containing supplier data.
        """
        # Convert to DataFrame
        self.df = pd.DataFrame(suppliers_data)
        
        # Try to use the database-trained model first
        model_used = "basic_weighted"
        try:
            from src.models.supplier_model import SupplierModel, normalize_supplier_data
            
            # Check if database-trained model exists
            model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'models')
            db_model_path = os.path.join(model_dir, 'supplier_model_from_db.h5')
            
            if os.path.exists(db_model_path):
                # Use database-trained model
                model = SupplierModel(db_model_path)
                
                # Normalize data
                X = normalize_supplier_data(self.df)
                
                # Get predictions
                predictions = model.predict(X)
                
                # Add predictions to dataframe
                self.df['predicted_score'] = predictions.flatten()
                
                # Sort by predicted score
                self.df = self.df.sort_values('predicted_score', ascending=False)
                
                model_used = "ml_model"
            else:
                # Fall back to weighted calculation
                self._calculate_weighted_scores()
        except Exception as e:
            print(f"Error using ML model: {e}")
            # Fall back to weighted calculation
            self._calculate_weighted_scores()
        
        # Save optimization results to database
        main_window = self.get_main_window()
        if main_window and hasattr(main_window, 'db'):
            # Save optimization with description
            optimization_id = main_window.db.save_optimization(
                self.df,
                f"Optimization run with {len(suppliers_data)} suppliers using {model_used}"
            )
            
            # Log activity
            main_window.db.log_activity(
                'optimize',
                f'Generated optimization results using {model_used}',
                f'Optimized {len(suppliers_data)} suppliers'
            )
        
        # Update UI
        self.update_ui()
    
    def _calculate_weighted_scores(self):
        """Calculate predicted scores using a simple weighted approach."""
        if self.df is None or len(self.df) == 0:
            return

        # Normalize features for model input
        normalized_df = self.df.copy()
        for col in ['cost', 'co2', 'delivery_time']:
            min_val = normalized_df[col].min()
            max_val = normalized_df[col].max()
            if max_val > min_val:
                normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
            else:
                normalized_df[col] = 0.5  # Default if all values are the same
        
        # Invert cost, CO2, and delivery time (lower is better)
        for col in ['cost', 'co2', 'delivery_time']:
            normalized_df[col] = 1 - normalized_df[col]
        
        # Ensure ethical score is calculated if not present
        if 'ethical_score' not in normalized_df.columns:
            # Calculate a synthetic ethical score based on other metrics
            normalized_df['ethical_score'] = (
                normalized_df['cost'] * 0.3 + 
                normalized_df['co2'] * 0.4 + 
                normalized_df['delivery_time'] * 0.3
            ) * 100
            
            # Add to original dataframe as well
            self.df['ethical_score'] = normalized_df['ethical_score']
        else:
            # Normalize ethical score if it's already present (scale to 0-1)
            normalized_df['ethical_score'] = normalized_df['ethical_score'] / 100
        
        # Calculate predicted scores
        # Weights for each feature
        weights = {
            'cost': 0.3,
            'co2': 0.2,
            'delivery_time': 0.2,
            'ethical_score': 0.3
        }
        
        # Calculate weighted scores
        self.df['predicted_score'] = (
            normalized_df['cost'] * weights['cost'] +
            normalized_df['co2'] * weights['co2'] +
            normalized_df['delivery_time'] * weights['delivery_time'] +
            normalized_df['ethical_score'] * weights['ethical_score']
        ) * 100
        
        # Sort by predicted score
        self.df = self.df.sort_values('predicted_score', ascending=False)
    
    def update_ui(self):
        """Update the UI with the latest data."""
        # Update the UI with the current data
        if hasattr(self, 'tabs'):
            # Clear existing tabs
            while self.tabs.count() > 0:
                self.tabs.removeTab(0)
            
            # Setup tabs again
            self.setup_tabs()
    
    def _get_critical_threshold(self):
        """Determine a critical threshold based on the data."""
        # Find gaps in the distribution of scores
        ethical_scores = sorted(self.df['ethical_score'])
        
        max_gap = 0
        threshold = 50.0  # Default threshold
        
        for i in range(1, len(ethical_scores)):
            gap = ethical_scores[i] - ethical_scores[i-1]
            if gap > max_gap:
                max_gap = gap
                threshold = (ethical_scores[i] + ethical_scores[i-1]) / 2
        
        # Determine the metric with the most significant threshold
        if threshold < 40 or threshold > 60:
            return f"An ethical score of {threshold:.1f}"
        
        # Look at other metrics
        cost_threshold = np.percentile(self.df['cost'], 75)
        if cost_threshold > self.df['cost'].mean() * 1.2:
            return f"A cost threshold of ${cost_threshold:.2f}"
        
        co2_threshold = np.percentile(self.df['co2'], 75)
        if co2_threshold > self.df['co2'].mean() * 1.2:
            return f"A CO2 emission level of {co2_threshold:.1f}kg"
        
        delivery_threshold = np.percentile(self.df['delivery_time'], 75)
        return f"A delivery time of {delivery_threshold:.1f} days"
    
    def _get_weight_adjustment(self):
        """Calculate suggested weight adjustments based on data distribution."""
        # Calculate correlations
        correlations = {
            'cost': abs(self.df['cost'].corr(self.df['predicted_score'])),
            'co2': abs(self.df['co2'].corr(self.df['predicted_score'])),
            'delivery_time': abs(self.df['delivery_time'].corr(self.df['predicted_score'])),
            'ethical_score': abs(self.df['ethical_score'].corr(self.df['predicted_score']))
        }
        
        # Normalize correlations
        total_corr = sum(correlations.values())
        if total_corr > 0:
            normalized = {k: v/total_corr for k, v in correlations.items()}
            return normalized['ethical_score'] * 10  # Scale to 0-10 range
        return 5  # Default middle value

    def create_supplier_network(self, layout):
        """Create a network diagram of suppliers.
        
        Args:
            layout (QVBoxLayout): Layout to add the network to.
        """
        # Create title
        title = QLabel("Supplier Relationship Network")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Create description
        description = QLabel(
            "This network diagram shows relationships between suppliers based on "
            "similarity in performance metrics. Connected suppliers have similar "
            "performance characteristics and could be potential alternatives."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(description)
        
        # Create controls frame
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        controls_layout = QHBoxLayout(controls_frame)
        
        # Add metric selection
        metric_label = QLabel("Metric:")
        metric_label.setStyleSheet("font-weight: bold;")
        self.metric_combo = QComboBox()
        self.metric_combo.addItems([
            "All Metrics", 
            "Cost", 
            "CO2 Emissions", 
            "Delivery Time", 
            "Ethical Score"
        ])
        
        # Add threshold selection
        threshold_label = QLabel("Connection Threshold:")
        threshold_label.setStyleSheet("font-weight: bold;")
        self.threshold_spinner = QSpinBox()
        self.threshold_spinner.setRange(1, 100)
        self.threshold_spinner.setValue(50)
        self.threshold_spinner.setSuffix("%")
        
        # Add update button
        update_button = QPushButton("Update Network")
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0069D9;
            }
        """)
        
        # Add controls to layout
        controls_layout.addWidget(metric_label)
        controls_layout.addWidget(self.metric_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(threshold_label)
        controls_layout.addWidget(self.threshold_spinner)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(update_button)
        controls_layout.addStretch()
        
        layout.addWidget(controls_frame)
        
        # Create network view
        web_view = QWebEngineView()
        web_view.setMinimumHeight(600)
        layout.addWidget(web_view)
        
        # Generate initial network
        if self.df is not None and len(self.df) > 0:
            self._generate_network_diagram(self.df, metric="All Metrics", threshold=0.5, web_view=web_view)
        else:
            # Display a message when no data is available
            self._display_no_data_message(web_view)
        
        # Connect update button
        update_button.clicked.connect(lambda: self._update_network_diagram(
            web_view,
            self.metric_combo.currentText(),
            self.threshold_spinner.value() / 100
        ))
    
    def _display_no_data_message(self, web_view, error_message=None):
        """Display a message when no data is available for visualization.
        
        Args:
            web_view (QWebEngineView): WebView to display the message in
            error_message (str, optional): Optional error message to display. Defaults to None.
        """
        message = error_message or "No supplier data available to display. Please add suppliers in the Input page."
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    color: #495057;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .message-container {{
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    padding: 30px;
                    max-width: 500px;
                }}
                h2 {{
                    color: #0056b3;
                    margin-bottom: 15px;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                }}
                .icon {{
                    font-size: 48px;
                    margin-bottom: 20px;
                    color: #6c757d;
                }}
            </style>
        </head>
        <body>
            <div class="message-container">
                <div class="icon">📊</div>
                <h2>No Data Available</h2>
                <p>{message}</p>
            </div>
        </body>
        </html>
        """
        web_view.setHtml(html)
    
    def _update_network_diagram(self, web_view, metric, threshold):
        """Update the network diagram with new settings.
        
        Args:
            web_view (QWebEngineView): Web view to update.
            metric (str): Metric to use for connections.
            threshold (float): Threshold for connections.
        """
        # Generate network diagram
        if self.df is not None and len(self.df) > 0:
            self._generate_network_diagram(self.df, metric, threshold, web_view)
        else:
            self._display_no_data_message(web_view)
        
        # Log activity
        main_window = self.get_main_window()
        if main_window and hasattr(main_window, 'db'):
            main_window.db.log_activity(
                'visualization',
                'Updated supplier network diagram',
                f'Metric: {metric}, Threshold: {threshold:.2f}'
            )
    
    def _generate_network_diagram(self, suppliers, metric="All Metrics", threshold=0.5, web_view=None):
        """Generate a network diagram based on the given metric and threshold.
        
        Args:
            suppliers (DataFrame): DataFrame containing supplier data
            metric (str, optional): Metric to use for node sizing. Defaults to "All Metrics".
            threshold (float, optional): Threshold for connection display. Defaults to 0.5.
            web_view (QWebEngineView, optional): WebView to display the diagram. Defaults to None.
            
        Returns:
            bool: True if diagram was generated successfully, False otherwise
        """
        try:
            if suppliers is None or len(suppliers) == 0:
                if web_view:
                    self._display_no_data_message(web_view)
                return False
            
            # Make a copy to avoid modifying the original
            suppliers = suppliers.copy()
            
            # Ensure suppliers have names
            if 'name' not in suppliers.columns:
                suppliers['name'] = [f"Supplier {i+1}" for i in range(len(suppliers))]
            
            # Convert to numeric
            for col in ['cost', 'co2', 'delivery_time']:
                if col in suppliers.columns:
                    suppliers[col] = pd.to_numeric(suppliers[col], errors='coerce')
                else:
                    suppliers[col] = 50  # Default value if column doesn't exist
            
            # Calculate normalized values (lower is better, so invert)
            for col in ['cost', 'co2', 'delivery_time']:
                if col in suppliers.columns:
                    min_val = suppliers[col].min()
                    max_val = suppliers[col].max()
                    if max_val > min_val:
                        suppliers[f'{col}_norm'] = 1 - (suppliers[col] - min_val) / (max_val - min_val)
                    else:
                        suppliers[f'{col}_norm'] = 0.5
                else:
                    suppliers[f'{col}_norm'] = 0.5
            
            # Use predicted_score or calculate ethical_score
            if 'predicted_score' in suppliers.columns:
                suppliers['score'] = suppliers['predicted_score']
            elif 'ethical_score' in suppliers.columns:
                suppliers['score'] = suppliers['ethical_score']
            else:
                # Calculate a simple ethical score based on normalized metrics
                suppliers['score'] = (
                    suppliers['cost_norm'] * 0.3 + 
                    suppliers['co2_norm'] * 0.4 + 
                    suppliers['delivery_time_norm'] * 0.3
                ) * 100
            
            # Normalize the score for visualization
            max_score = suppliers['score'].max()
            if max_score > 0:
                suppliers['score_norm'] = suppliers['score'] / max_score
            else:
                suppliers['score_norm'] = 0.5
            
            # Create node positions in a circle
            n = len(suppliers)
            positions = []
            for i in range(n):
                angle = 2 * math.pi * i / n
                positions.append((math.cos(angle), math.sin(angle)))
            
            # Create edges between nodes (connections between similar suppliers)
            edges = []
            for i in range(n):
                for j in range(i+1, n):
                    # Calculate similarity based on normalized metrics
                    similarity = 0
                    if metric == "Cost":
                        similarity = 1 - abs(suppliers['cost_norm'].iloc[i] - suppliers['cost_norm'].iloc[j])
                    elif metric == "CO2":
                        similarity = 1 - abs(suppliers['co2_norm'].iloc[i] - suppliers['co2_norm'].iloc[j])
                    elif metric == "Delivery Time":
                        similarity = 1 - abs(suppliers['delivery_time_norm'].iloc[i] - suppliers['delivery_time_norm'].iloc[j])
                    else:  # All Metrics
                        similarity = (
                            (1 - abs(suppliers['cost_norm'].iloc[i] - suppliers['cost_norm'].iloc[j])) * 0.3 +
                            (1 - abs(suppliers['co2_norm'].iloc[i] - suppliers['co2_norm'].iloc[j])) * 0.4 +
                            (1 - abs(suppliers['delivery_time_norm'].iloc[i] - suppliers['delivery_time_norm'].iloc[j])) * 0.3
                        )
                    
                    if similarity > threshold:
                        edges.append((i, j, similarity))
            
            # Create a plotly figure
            fig = go.Figure()
            
            # Add edges as lines
            for i, j, strength in edges:
                fig.add_trace(go.Scatter(
                    x=[positions[i][0], positions[j][0], None],
                    y=[positions[i][1], positions[j][1], None],
                    mode='lines',
                    line=dict(width=strength*3, color='rgba(150,150,150,0.7)'),
                    hoverinfo='none',
                    showlegend=False
                ))
            
            # Add nodes as scatter points
            node_sizes = []
            node_colors = []
            hover_texts = []
            
            for i, (_, row) in enumerate(suppliers.iterrows()):
                # Set node size based on metric
                if metric == "Cost":
                    size = row['cost_norm'] * 30 + 10
                elif metric == "CO2":
                    size = row['co2_norm'] * 30 + 10
                elif metric == "Delivery Time":
                    size = row['delivery_time_norm'] * 30 + 10
                else:  # All Metrics
                    size = row['score_norm'] * 30 + 10
                
                node_sizes.append(size)
                node_colors.append(row['score'])
                
                # Create hover text
                hover_text = f"<b>{row['name']}</b><br>"
                if 'cost' in row:
                    hover_text += f"Cost: ${row['cost']:.2f}<br>"
                if 'co2' in row:
                    hover_text += f"CO2: {row['co2']:.1f} kg<br>"
                if 'delivery_time' in row:
                    hover_text += f"Delivery: {row['delivery_time']:.1f} days<br>"
                hover_text += f"Score: {row['score']:.1f}<br>"
                hover_text += f"Connections: {sum(1 for e in edges if i in (e[0], e[1]))}"
                
                hover_texts.append(hover_text)
            
            # Add nodes
            fig.add_trace(go.Scatter(
                x=[p[0] for p in positions],
                y=[p[1] for p in positions],
                mode='markers+text',
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    colorscale='Viridis',
                    colorbar=dict(title='Score'),
                    line=dict(width=1, color='black')
                ),
                text=suppliers['name'],
                textposition='top center',
                hovertext=hover_texts,
                hoverinfo='text',
                showlegend=False
            ))
            
            # Set layout
            fig.update_layout(
                title=f"Supplier Network - {metric}",
                showlegend=False,
                hovermode='closest',
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(255,255,255,1)',
                height=600
            )
            
            # Convert to HTML and display
            html = fig.to_html(include_plotlyjs='cdn', full_html=False)
            
            if web_view:
                web_view.setHtml(html)
            
            return True
        except Exception as e:
            print(f"Error generating network diagram: {e}")
            traceback.print_exc()
            if web_view:
                self._display_no_data_message(web_view, f"Error generating network diagram: {e}")
            return False

    def create_explanation_content(self, layout):
        """Create explanation content for the explanation tab.
        
        Args:
            layout (QVBoxLayout): Layout to add content to
        """
        # Create a scroll area for the explanation content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create a widget to hold the content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Create styled HTML content with explanation
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                h1 { color: #2c3e50; font-size: 24px; margin-top: 20px; }
                h2 { color: #3498db; font-size: 20px; margin-top: 15px; }
                .section { margin-bottom: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 5px; }
                .highlight { color: #e74c3c; font-weight: bold; }
                .metric { font-weight: bold; color: #2980b9; }
                ol { padding-left: 20px; }
                li { margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h1>EthicSupply AI Analysis</h1>
            
            <div class="section">
                <h2>AI Model Overview</h2>
                <p>
                    The EthicSupply AI model has analyzed your supplier data and generated recommendations 
                    based on multiple factors including cost efficiency, environmental impact, and operational efficiency.
                </p>
                <p>
                    Our algorithm optimizes for the best balance of <span class="metric">cost</span>, 
                    <span class="metric">CO2 emissions</span>, and <span class="metric">delivery time</span> 
                    while maintaining high ethical standards.
                </p>
            </div>
            
            <div class="section">
                <h2>Ethical Score Calculation</h2>
                <p>
                    The ethical score is a comprehensive metric calculated based on:
                </p>
                <ul>
                    <li><span class="metric">Cost Efficiency (30%)</span>: Lower relative cost increases score</li>
                    <li><span class="metric">Environmental Impact (40%)</span>: Lower CO2 emissions increase score</li>
                    <li><span class="metric">Operational Efficiency (30%)</span>: Faster delivery times increase score</li>
                </ul>
                <p>
                    Each factor is normalized across all suppliers to ensure fair comparison.
                    Scores range from 0-100, with higher scores indicating more ethical suppliers.
                </p>
            </div>
            
            <div class="section">
                <h2>Top Suppliers Analysis</h2>
                <p>
                    Based on the data provided, our system has identified the following top suppliers:
                </p>
        """
        
        # Dynamically generate top suppliers section
        if self.df is not None and len(self.df) > 0:
            # Sort by predicted_score if available, otherwise by ethical_score
            sort_col = 'predicted_score' if 'predicted_score' in self.df.columns else 'ethical_score'
            if sort_col in self.df.columns:
                top_suppliers = self.df.sort_values(by=sort_col, ascending=False).head(3)
                
                for i, (_, supplier) in enumerate(top_suppliers.iterrows()):
                    name = supplier.get('name', f"Supplier {i+1}")
                    cost = supplier.get('cost', 0)
                    co2 = supplier.get('co2', 0)
                    delivery = supplier.get('delivery_time', 0)
                    ethical = supplier.get('ethical_score', 0) if 'ethical_score' in supplier else supplier.get('predicted_score', 0)
                    
                    html_content += f"""
                    <div style="margin-left: 20px; margin-bottom: 15px; padding: 10px; background-color: #f0f7fb; border-left: 5px solid #3498db;">
                        <h3>{name}</h3>
                        <ul>
                            <li>Cost: ${cost:.2f}</li>
                            <li>CO2 Emissions: {co2:.1f} kg</li>
                            <li>Delivery Time: {delivery:.1f} days</li>
                            <li>Ethical Score: {ethical:.1f} / 100</li>
                        </ul>
                        <p><strong>Recommendation:</strong> {self._get_supplier_recommendation(supplier)}</p>
                    </div>
                    """
        
        html_content += """
            </div>
            
            <div class="section">
                <h2>Performance Optimization Tips</h2>
                <p>
                    To improve your supply chain sustainability and ethics:
                </p>
                <ol>
                    <li>Consider replacing suppliers with ethical scores below 50</li>
                    <li>Prioritize suppliers with balanced scores across all metrics</li>
                    <li>When cost is equal, choose suppliers with better environmental metrics</li>
                    <li>Monitor your supplier performance trends over time using the dashboard</li>
                </ol>
            </div>
        </body>
        </html>
        """
        
        # Create a QTextBrowser to display the HTML content
        text_browser = QTextBrowser()
        text_browser.setHtml(html_content)
        text_browser.setOpenExternalLinks(True)
        
        content_layout.addWidget(text_browser)
        
        # Set the content widget as the scroll area widget
        scroll.setWidget(content_widget)
        
        # Add the scroll area to the layout
        layout.addWidget(scroll)
    
    def _get_supplier_recommendation(self, supplier):
        """Generate a recommendation for a supplier based on its metrics.
        
        Args:
            supplier (Series): Supplier data
            
        Returns:
            str: Recommendation text
        """
        cost = supplier.get('cost', 0)
        co2 = supplier.get('co2', 0)
        delivery = supplier.get('delivery_time', 0)
        
        # Simple recommendation logic based on strengths
        strengths = []
        
        if cost < 500:
            strengths.append("cost-effective")
        if co2 < 50:
            strengths.append("environmentally friendly")
        if delivery < 10:
            strengths.append("fast delivery")
            
        if not strengths:
            strengths.append("balanced performance")
            
        return f"This supplier offers {', '.join(strengths)} advantages to your supply chain."

    def create_action_buttons(self):
        """Create action buttons for navigating and exporting results."""
        button_layout = QHBoxLayout()
        
        # Back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard)
        button_layout.addWidget(back_btn)
        
        # Spacer
        button_layout.addStretch()
        
        # Export button
        export_btn = QPushButton("Export Results")
        export_btn.clicked.connect(self._export_dialog)
        button_layout.addWidget(export_btn)
        
        # Template button
        template_btn = QPushButton("Download Template")
        template_btn.clicked.connect(self.download_template)
        button_layout.addWidget(template_btn)
        
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
        
    def export_results(self, format='csv'):
        """Export results to a file.
        
        Args:
            format (str): Format to export to ('csv' or 'pdf').
        """
        if format == 'csv':
            # Export to CSV
            filename = f"optimization_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Create enhanced dataframe with additional information for export
            export_df = self.df.copy()
            
            # Add additional supplier information
            if 'supplier_id' not in export_df.columns:
                export_df['supplier_id'] = [f"SUP-{2023+i:04d}" for i in range(len(export_df))]
            
            if 'contact_email' not in export_df.columns:
                export_df['contact_email'] = [f"contact@{name.lower().replace(' ', '')}.com" for name in export_df['name']]
            
            # Add regional information (random assignment for sample data)
            if 'region' not in export_df.columns:
                regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
                export_df['region'] = [random.choice(regions) for _ in range(len(export_df))]
            
            # Add sustainability certifications
            if 'sustainability_cert' not in export_df.columns:
                certifications = ['ISO 14001', 'FSC Certified', 'B Corp Certified', 'Cradle to Cradle', 
                                'Fair Trade', 'EMAS', 'Rainforest Alliance', 'PEFC Certified']
                export_df['sustainability_cert'] = [random.choice(certifications) for _ in range(len(export_df))]
            
            # Add payment terms (random assignment for sample data)
            if 'payment_terms' not in export_df.columns:
                payment_terms = ['Net 30', 'Net 45', 'Net 60', 'Net 90']
                export_df['payment_terms'] = [random.choice(payment_terms) for _ in range(len(export_df))]
            
            # Add production capacity
            if 'production_capacity' not in export_df.columns:
                capacities = ['5000 units/month', '3000 units/month', '8000 units/month', '10000 units/month']
                export_df['production_capacity'] = [random.choice(capacities) for _ in range(len(export_df))]
            
            # Add order quantities
            if 'min_order_qty' not in export_df.columns:
                min_qtys = [50, 100, 200, 500]
                export_df['min_order_qty'] = [random.choice(min_qtys) for _ in range(len(export_df))]
            
            if 'max_order_qty' not in export_df.columns:
                max_qtys = [5000, 10000, 15000, 20000]
                export_df['max_order_qty'] = [random.choice(max_qtys) for _ in range(len(export_df))]
            
            # Add currency
            if 'currency' not in export_df.columns:
                currencies = ['USD', 'EUR', 'GBP', 'CAD']
                export_df['currency'] = [random.choice(currencies) for _ in range(len(export_df))]
            
            # Add certifications (multiple per supplier)
            if 'certifications' not in export_df.columns:
                all_certs = ['ISO 9001', 'ISO 14001', 'FSC', 'PEFC', 'B Corp', 'Fair Trade', 'Rainforest Alliance']
                export_df['certifications'] = [';'.join(random.sample(all_certs, k=random.randint(1, 3))) for _ in range(len(export_df))]
            
            # Add specialization
            if 'specialization' not in export_df.columns:
                specializations = ['Electronics', 'Packaging', 'Textiles', 'Food', 'Chemicals', 'Construction']
                export_df['specialization'] = [random.choice(specializations) for _ in range(len(export_df))]
            
            # Add website
            if 'website' not in export_df.columns:
                export_df['website'] = [f"https://www.{name.lower().replace(' ', '')}.com" for name in export_df['name']]
            
            # Select only the columns in our template format
            template_columns = [
                'name', 'supplier_id', 'cost', 'delivery_time', 'co2', 
                'contact_email', 'region', 'sustainability_cert', 'payment_terms', 
                'production_capacity', 'min_order_qty', 'max_order_qty', 'currency', 
                'certifications', 'specialization', 'website', 'predicted_score'
            ]
            
            # Ensure only columns that exist in the dataframe are used
            available_columns = [col for col in template_columns if col in export_df.columns]
            export_df = export_df[available_columns]
            
            # Export enhanced dataframe
            export_df.to_csv(filename, index=False)
            
            # Log activity
            main_window = self.get_main_window()
            if main_window and hasattr(main_window, 'db'):
                main_window.db.log_activity(
                    'export',
                    'Exported results to CSV',
                    f'File: {filename}'
                )
            
            # Show confirmation
            if main_window:
                main_window.show_status_message(f"Results exported to {filename}", 3000)
        elif format == 'pdf':
            # TODO: Implement PDF export
            pass

    def initialize_with_sample_data(self):
        """Initialize the results page with sample data if needed."""
        try:
            # Check if we can load data from the database
            main_window = self.get_main_window()
            if main_window and hasattr(main_window, 'db'):
                # Try to get the latest optimization
                db = main_window.db
                optimizations = db.get_optimizations(limit=1)
                
                if optimizations and len(optimizations) > 0:
                    # Load the data from the latest optimization
                    optimization_id = optimizations[0]['id']
                    results = db.get_optimization_results(optimization_id)
                    
                    if results and len(results) > 0:
                        # Use the results as our dataframe
                        self.df = pd.DataFrame(results)
                        self._calculate_weighted_scores()
                        self.update_ui()
                        return
            
            # If no data in the database, generate sample data
            self.generate_sample_data()
            
        except Exception as e:
            print(f"Error initializing with sample data: {e}")
            # Use an empty dataframe with the right columns
            self.df = pd.DataFrame(columns=['name', 'cost', 'co2', 'delivery_time', 'predicted_score'])

    def generate_sample_data(self):
        """Generate and set sample data for suppliers."""
        # Generate sample data for 15 suppliers
        suppliers = []
        
        for i in range(1, 16):
            supplier = {
                'name': f"Supplier_{i:04d}",
                'cost': random.uniform(100, 1000),
                'co2': random.uniform(100, 500),
                'delivery_time': random.uniform(1, 30)
                # Note: ethical_score is intentionally omitted as it will be calculated
            }
            suppliers.append(supplier)
        
        # Create DataFrame
        self.df = pd.DataFrame(suppliers)
        
        # Calculate weighted scores and this will also add ethical_score
        self._calculate_weighted_scores()
        
        # Update UI
        self.update_ui()

    def download_template(self):
        """Download a CSV template for supplier data."""
        # Create template file path
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_path = os.path.join(app_dir, 'supplier_export_template.csv')
        
        # Create or ensure template exists
        template_path = self.create_template_file(template_path)
        
        # Get save location from user
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(
            self,
            "Save Supplier Template",
            "supplier_template.csv",
            "CSV Files (*.csv)"
        )
        
        if save_path:
            # Copy template to user-selected location
            import shutil
            try:
                shutil.copy(template_path, save_path)
                
                # Log activity
                main_window = self.get_main_window()
                if main_window and hasattr(main_window, 'db'):
                    main_window.db.log_activity(
                        'export',
                        'Downloaded CSV template',
                        f'File: {save_path}'
                    )
                
                # Show confirmation
                if main_window:
                    main_window.show_status_message(f"Template downloaded to {save_path}", 3000)
            except Exception as e:
                # Show error
                if main_window:
                    main_window.show_status_message(f"Error downloading template: {str(e)}", 5000, error=True) 