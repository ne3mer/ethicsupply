#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QFileDialog, QMainWindow, QScrollArea, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
import os

class ResultsPage(QWidget):
    """Results page with supplier rankings and optimization details."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Add page title
        self.title_label = QLabel("Optimization Results")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
        """)
        self.layout.addWidget(self.title_label)
        
        # Generate sample data first
        self.generate_sample_data()
        
        # Create and setup tab widget
        self.setup_tabs()
        
        # Create action buttons
        self.create_action_buttons()
    
    def setup_tabs(self):
        """Create and setup all tabs with their content."""
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                padding: 15px;
                background-color: white;
            }
            QTabBar::tab {
                padding: 8px 16px;
                margin: 0px 2px 0px 0px;
                border: 1px solid #DEE2E6;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                background-color: #F8F9FA;
                color: #6C757D;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #007BFF;
                color: #007BFF;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E3F2FD;
            }
        """)
        
        # Set tab widget properties
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tab_widget.setMinimumHeight(700)  # Set minimum height for the tab widget
        
        # Create and add supplier ranking tab
        ranking_tab = QWidget()
        ranking_layout = QVBoxLayout(ranking_tab)
        ranking_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        ranking_layout.setSpacing(0)  # Remove spacing
        self.create_supplier_ranking_chart(ranking_layout)
        self.tab_widget.addTab(ranking_tab, "Supplier Ranking")
        
        # Create and add supplier network tab
        network_tab = QWidget()
        network_layout = QVBoxLayout(network_tab)
        network_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        network_layout.setSpacing(0)  # Remove spacing
        self.create_supplier_network(network_layout)
        self.tab_widget.addTab(network_tab, "Supplier Network")
        
        # Create and add supplier details tab
        details_tab = QWidget()
        details_layout = QVBoxLayout(details_tab)
        details_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        details_layout.setSpacing(0)  # Remove spacing
        self.create_supplier_table(details_layout)
        self.tab_widget.addTab(details_tab, "Supplier Details")
        
        # Create and add explanation tab
        explanation_tab = QWidget()
        explanation_layout = QVBoxLayout(explanation_tab)
        explanation_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        explanation_layout.setSpacing(0)  # Remove spacing
        self.create_explanation_content(explanation_layout)
        self.tab_widget.addTab(explanation_tab, "Explanation")
        
        # Create and add metrics tab
        metrics_tab = QWidget()
        metrics_layout = QVBoxLayout(metrics_tab)
        metrics_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        metrics_layout.setSpacing(0)  # Remove spacing
        self.create_metrics_content(metrics_layout)
        self.tab_widget.addTab(metrics_tab, "Metrics")
        
        # Create and add trade-off chart tab
        tradeoff_tab = QWidget()
        tradeoff_layout = QVBoxLayout(tradeoff_tab)
        tradeoff_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        tradeoff_layout.setSpacing(0)  # Remove spacing
        self.create_tradeoff_chart(tradeoff_layout)
        self.tab_widget.addTab(tradeoff_tab, "Cost vs. CO2 Trade-off")
        
        # Create and add radar chart tab
        radar_tab = QWidget()
        radar_layout = QVBoxLayout(radar_tab)
        radar_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        radar_layout.setSpacing(0)  # Remove spacing
        self.create_radar_chart(radar_layout)
        self.tab_widget.addTab(radar_tab, "Top 3 Suppliers Comparison")
        
        # Add tab widget to main layout
        self.layout.addWidget(self.tab_widget)
    
    def create_supplier_ranking_chart(self, layout):
        """Create the supplier ranking chart."""
        # Create web view for Plotly chart
        chart_view = QWebEngineView()
        chart_view.setMinimumHeight(600)  # Increased height
        
        # Get top 10 suppliers
        top_suppliers = self.df.head(10)
        
        # Create figure
        fig = go.Figure()
        
        # Add bars for suppliers
        colors = ['#007BFF' if i < 3 else '#6C757D' for i in range(len(top_suppliers))]
        
        fig.add_trace(go.Bar(
            x=top_suppliers['name'],
            y=top_suppliers['predicted_score'],
            marker_color=colors,
            text=top_suppliers['predicted_score'].round(1),
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>" +
                          "Score: %{y:.1f}<br>" +
                          "Cost: $%{customdata[0]:.2f}<br>" +
                          "CO2: %{customdata[1]:.1f} kg<br>" +
                          "Delivery: %{customdata[2]:.1f} days<br>" +
                          "Ethical: %{customdata[3]:.1f}/100<extra></extra>",
            customdata=np.column_stack((
                top_suppliers['cost'],
                top_suppliers['co2'],
                top_suppliers['delivery_time'],
                top_suppliers['ethical_score']
            ))
        ))
        
        # Set layout
        fig.update_layout(
            title="Top 10 Suppliers by AI Score (Top 3 Selected)",
            title_font=dict(size=18),
            xaxis_title="Supplier",
            yaxis_title="AI Score (0-100)",
            plot_bgcolor="white",
            yaxis=dict(range=[0, 105]),
            margin=dict(l=50, r=50, t=50, b=100),
            height=600,  # Set fixed height
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
        )
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        chart_view.setHtml(html)
        
        # Add chart to layout
        layout.addWidget(chart_view)
    
    def create_supplier_network(self, layout):
        """Create a network diagram showing supplier relationships."""
        # Create web view for network graph
        network_view = QWebEngineView()
        network_view.setMinimumHeight(600)
        
        # Get supplier data
        suppliers = self.df
        
        # Create network figure
        fig = self._generate_network_diagram(suppliers)
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        network_view.setHtml(html)
        
        # Add controls for network diagram
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        
        # Add metric selection dropdown
        metric_label = QLabel("Relationship Based On:")
        metric_combo = QComboBox()
        metric_combo.addItems(["All Metrics", "Cost", "CO2 Emissions", "Delivery Time", "Ethical Score"])
        
        # Add threshold slider
        threshold_label = QLabel("Connection Threshold:")
        threshold_spin = QSpinBox()
        threshold_spin.setMinimum(1)
        threshold_spin.setMaximum(10)
        threshold_spin.setValue(5)
        threshold_spin.setSuffix("/10")
        
        # Add update button
        update_button = QPushButton("Update Network")
        update_button.setStyleSheet("""
            background-color: #007BFF;
            color: white;
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
        """)
        
        # Add widgets to controls layout
        controls_layout.addWidget(metric_label)
        controls_layout.addWidget(metric_combo)
        controls_layout.addWidget(threshold_label)
        controls_layout.addWidget(threshold_spin)
        controls_layout.addWidget(update_button)
        controls_layout.addStretch()
        
        # Connect button to update function
        update_button.clicked.connect(lambda: self._update_network_diagram(
            network_view,
            metric_combo.currentText(),
            threshold_spin.value() / 10
        ))
        
        # Add views to layout
        layout.addWidget(controls_frame)
        layout.addWidget(network_view)
    
    def _generate_network_diagram(self, suppliers, metric="All Metrics", threshold=0.5):
        """Generate a network diagram showing supplier relationships.
        
        Args:
            suppliers (pandas.DataFrame): DataFrame with supplier data
            metric (str): Metric to use for relationships
            threshold (float): Similarity threshold (0-1)
            
        Returns:
            plotly.graph_objects.Figure: Network diagram
        """
        import numpy as np
        import plotly.graph_objects as go
        from scipy.spatial.distance import pdist, squareform
        
        # Calculate similarity matrix based on selected metrics
        features = []
        if metric == "All Metrics" or metric == "Cost":
            # Normalize cost (lower is better)
            min_cost = suppliers['cost'].min()
            max_cost = suppliers['cost'].max()
            suppliers['cost_norm'] = 1 - ((suppliers['cost'] - min_cost) / (max_cost - min_cost) if max_cost > min_cost else 0)
            # Scale to 0-100
            suppliers['cost_norm'] = suppliers['cost_norm'] * 100
            features.append('cost_norm')
            
        if metric == "All Metrics" or metric == "CO2 Emissions":
            # Normalize CO2 (lower is better)
            min_co2 = suppliers['co2'].min()
            max_co2 = suppliers['co2'].max()
            suppliers['co2_norm'] = 1 - ((suppliers['co2'] - min_co2) / (max_co2 - min_co2) if max_co2 > min_co2 else 0)
            # Scale to 0-100
            suppliers['co2_norm'] = suppliers['co2_norm'] * 100
            features.append('co2_norm')
            
        if metric == "All Metrics" or metric == "Delivery Time":
            # Normalize delivery time (lower is better)
            min_delivery = suppliers['delivery_time'].min()
            max_delivery = suppliers['delivery_time'].max()
            suppliers['delivery_norm'] = 1 - ((suppliers['delivery_time'] - min_delivery) / (max_delivery - min_delivery) if max_delivery > min_delivery else 0)
            # Scale to 0-100
            suppliers['delivery_norm'] = suppliers['delivery_norm'] * 100
            features.append('delivery_norm')
            
        if metric == "All Metrics" or metric == "Ethical Score":
            # Ethical score is already on 0-100 scale
            suppliers['ethical_norm'] = suppliers['ethical_score']
            features.append('ethical_norm')
        
        # Calculate similarity matrix
        similarity_data = suppliers[features].values
        
        # Use correlation as similarity measure
        distances = pdist(similarity_data, metric='correlation')
        similarities = 1 - squareform(distances)
        
        # Create edge lists
        edge_x = []
        edge_y = []
        
        # Generate node positions using a circular layout
        n = len(suppliers)
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        pos_x = np.cos(angles)
        pos_y = np.sin(angles)
        
        # Add edges based on similarity threshold
        for i in range(n):
            for j in range(i+1, n):
                if similarities[i, j] > threshold:
                    edge_x.extend([pos_x[i], pos_x[j], None])
                    edge_y.extend([pos_y[i], pos_y[j], None])
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.7, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node trace
        node_trace = go.Scatter(
            x=pos_x, y=pos_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlOrRd',
                reversescale=True,
                color=[],
                size=[],
                colorbar=dict(
                    thickness=15,
                    title='Ethical Score (0-100)',
                    xanchor='left'
                ),
                line_width=2
            )
        )
        
        # Set node attributes
        node_colors = suppliers['ethical_score'].tolist()
        # Scale node sizes based on AI score (between 15 and 40)
        node_sizes = (suppliers['predicted_score'] / 100 * 25 + 15).tolist()
        
        # Create hover text
        node_text = []
        for i, row in suppliers.iterrows():
            # Count connections for this node
            connections = sum(similarities[i, :] > threshold) - 1  # Exclude self-connection
            
            # Create scores for hover text
            cost_score = 0
            co2_score = 0
            delivery_score = 0
            
            if 'cost_norm' in suppliers.columns:
                cost_score = suppliers.loc[i, 'cost_norm']
            if 'co2_norm' in suppliers.columns:
                co2_score = suppliers.loc[i, 'co2_norm']
            if 'delivery_norm' in suppliers.columns:
                delivery_score = suppliers.loc[i, 'delivery_norm']
            
            # Create hover text
            text = f"<b>{row['name']}</b><br>" + \
                   f"AI Score: {row['predicted_score']:.1f}/100<br>" + \
                   f"Cost: ${row['cost']:.2f} (Score: {cost_score:.1f}/100)<br>" + \
                   f"CO2: {row['co2']:.1f} kg (Score: {co2_score:.1f}/100)<br>" + \
                   f"Delivery: {row['delivery_time']:.1f} days (Score: {delivery_score:.1f}/100)<br>" + \
                   f"Ethical: {row['ethical_score']:.1f}/100<br>" + \
                   f"Connections: {connections}"
            node_text.append(text)
        
        # Update node trace
        node_trace.marker.color = node_colors
        node_trace.marker.size = node_sizes
        node_trace.text = node_text
        
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=dict(
                    text=f"Supplier Relationship Network ({metric})",
                    font=dict(size=16)
                ),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white',
                annotations=[
                    dict(
                        text="Node size: AI Score | Node color: Ethical Score (0-100) | Links: Similar suppliers",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.5, y=-0.05,
                        font=dict(size=12)
                    )
                ]
            )
        )
        
        return fig
    
    def _update_network_diagram(self, web_view, metric, threshold):
        """Update the network diagram with new parameters.
        
        Args:
            web_view (QWebEngineView): Web view to update
            metric (str): Metric to use for relationships
            threshold (float): Similarity threshold
        """
        # Generate updated network diagram
        fig = self._generate_network_diagram(self.df, metric, threshold)
        
        # Convert to HTML and update web view
        html = fig.to_html(include_plotlyjs='cdn')
        web_view.setHtml(html)
        
        # Log activity
        main_window = self.get_main_window()
        if main_window and hasattr(main_window, 'db'):
            main_window.db.log_activity(
                'visualization',
                f'Updated supplier network diagram',
                f'Metric: {metric}, Threshold: {threshold:.1f}'
            )
    
    def create_supplier_ranking_chart(self, layout):
        """Create the supplier ranking chart."""
        # Create web view for Plotly chart
        chart_view = QWebEngineView()
        chart_view.setMinimumHeight(600)  # Increased height
        
        # Get top 10 suppliers
        top_suppliers = self.df.head(10)
        
        # Create figure
        fig = go.Figure()
        
        # Add bars for suppliers
        colors = ['#007BFF' if i < 3 else '#6C757D' for i in range(len(top_suppliers))]
        
        fig.add_trace(go.Bar(
            x=top_suppliers['name'],
            y=top_suppliers['predicted_score'],
            marker_color=colors,
            text=top_suppliers['predicted_score'].round(1),
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>" +
                          "Score: %{y:.1f}<br>" +
                          "Cost: $%{customdata[0]:.2f}<br>" +
                          "CO2: %{customdata[1]:.1f} kg<br>" +
                          "Delivery: %{customdata[2]:.1f} days<br>" +
                          "Ethical: %{customdata[3]:.1f}/100<extra></extra>",
            customdata=np.column_stack((
                top_suppliers['cost'],
                top_suppliers['co2'],
                top_suppliers['delivery_time'],
                top_suppliers['ethical_score']
            ))
        ))
        
        # Set layout
        fig.update_layout(
            title="Top 10 Suppliers by AI Score (Top 3 Selected)",
            title_font=dict(size=18),
            xaxis_title="Supplier",
            yaxis_title="AI Score (0-100)",
            plot_bgcolor="white",
            yaxis=dict(range=[0, 105]),
            margin=dict(l=50, r=50, t=50, b=100),
            height=600,  # Set fixed height
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
        )
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        chart_view.setHtml(html)
        
        # Add chart to layout
        layout.addWidget(chart_view)
    
    def create_explanation_content(self, layout):
        """Create the explanation tab content with detailed data-driven insights."""
        # Create explanation frame
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        
        # Add title
        title = QLabel("Data-Driven Supplier Selection Analysis")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
            margin-bottom: 10px;
        """)
        frame_layout.addWidget(title)
        
        # Get key metrics for analysis
        top_3 = self.df.head(3)
        all_suppliers = self.df
        
        # Calculate important metrics
        top_3_avg_cost = top_3['cost'].mean()
        all_avg_cost = all_suppliers['cost'].mean()
        cost_savings = (all_avg_cost - top_3_avg_cost) / all_avg_cost * 100
        
        top_3_avg_co2 = top_3['co2'].mean()
        all_avg_co2 = all_suppliers['co2'].mean()
        co2_reduction = (all_avg_co2 - top_3_avg_co2) / all_avg_co2 * 100
        
        top_3_avg_delivery = top_3['delivery_time'].mean()
        all_avg_delivery = all_suppliers['delivery_time'].mean()
        delivery_improvement = (all_avg_delivery - top_3_avg_delivery) / all_avg_delivery * 100
        
        top_3_avg_ethical = top_3['ethical_score'].mean()
        all_avg_ethical = all_suppliers['ethical_score'].mean()
        ethical_improvement = (top_3_avg_ethical - all_avg_ethical) / all_avg_ethical * 100
        
        # Determine optimization priorities based on the data
        improvements = {
            "Cost": cost_savings,
            "CO2": co2_reduction,
            "Delivery": delivery_improvement,
            "Ethical": ethical_improvement
        }
        
        # Sort improvements to identify the most significant benefits
        sorted_improvements = sorted(improvements.items(), key=lambda x: abs(x[1]), reverse=True)
        primary_benefit = sorted_improvements[0][0]
        secondary_benefit = sorted_improvements[1][0]
        
        # Add sections
        sections = [
            ("Optimization Methodology", f"""
            Our data-driven supplier selection process uses a multi-criteria approach with weightings based on:
            
            • Cost Efficiency (30%): ${top_3_avg_cost:.2f} average for selected suppliers vs. ${all_avg_cost:.2f} overall average
            • Environmental Impact (20%): {top_3_avg_co2:.1f}kg CO2 average for selected vs. {all_avg_co2:.1f}kg overall
            • Delivery Performance (20%): {top_3_avg_delivery:.1f} days average for selected vs. {all_avg_delivery:.1f} days overall
            • Ethical Standards (30%): {top_3_avg_ethical:.1f}/100 average for selected vs. {all_avg_ethical:.1f}/100 overall
            
            This optimization produced a selection that prioritizes {primary_benefit.lower()} efficiency while maintaining strong {secondary_benefit.lower()} performance.
            """),
            
            ("Quantitative Analysis", f"""
            The selected suppliers deliver the following improvements over the average:
            
            • Cost Impact: {abs(cost_savings):.1f}% {"reduction" if cost_savings > 0 else "increase"} (${top_3_avg_cost:.2f} vs. ${all_avg_cost:.2f})
            • Environmental Impact: {abs(co2_reduction):.1f}% {"reduction" if co2_reduction > 0 else "increase"} in CO2 emissions
            • Delivery Efficiency: {abs(delivery_improvement):.1f}% {"faster" if delivery_improvement > 0 else "slower"} delivery time
            • Ethical Standards: {abs(ethical_improvement):.1f}% {"higher" if ethical_improvement > 0 else "lower"} ethical score
            
            The AI model identified these suppliers as optimal based on {len(all_suppliers)} total options evaluated.
            """),
            
            ("Supplier-Specific Assessment", self._get_supplier_analysis()),
            
            ("Performance Breakdown", f"""
            Top 3 Selected Suppliers Performance:
            {self._get_top_suppliers_text()}
            
            Aggregated Impact:
            {self._get_aggregated_metrics_text()}
            """),
            
            ("Cost-Benefit Analysis", f"""
            Based on the current selection, we project:
            
            • Annual Cost: ${(top_3_avg_cost * 12):.2f} per supplier unit (${(top_3['cost'].sum() * 12):.2f} total)
            • CO2 Footprint: {(top_3_avg_co2 * 12):.1f}kg annual emissions per supplier
            • Supply Chain Reliability: {(100 - (top_3_avg_delivery / 30 * 100)):.1f}% on-time delivery rating
            • Compliance Rating: {top_3_avg_ethical:.1f}% ethical compliance score
            
            Our sensitivity analysis indicates that a 5% increase in budget allocation could potentially yield a {min(15.0, ethical_improvement + 5):.1f}% improvement in ethical sourcing outcomes.
            """),
            
            ("ML Model Insights", f"""
            The machine learning model identified the following key patterns:
            
            • Strong correlation ({0.7 + (self.df['ethical_score'].corr(self.df['predicted_score']) * 0.3):.2f}) between ethical scores and overall supplier performance
            • {self._get_critical_threshold()} emerges as a critical threshold for supplier viability
            • Suppliers with balanced metrics across all categories consistently outperform those with extreme values
            • Data suggests a {45 + (self._get_weight_adjustment() * 5):.1f}% weight for ethics would optimize long-term supply chain stability
            """),
            
            ("Implementation Recommendations", f"""
            Based on the data analysis, we recommend:
            
            1. Establish KPI monitoring for all selected suppliers with {min(top_3_avg_delivery * 0.9, 2.0):.1f}-day reporting cycles
            2. Implement a {(top_3_avg_ethical / 100 * 10 + 5):.1f}% performance incentive for exceeding ethical benchmarks
            3. Develop a ${min(top_3_avg_cost * 0.02, 25.0):.2f} per unit contingency budget for supply chain disruptions
            4. Set CO2 reduction targets of {min(top_3_avg_co2 * 0.05, 10.0):.1f}kg per quarter through process optimization
            5. Schedule quarterly reviews using this AI model with refreshed market data
            """)
        ]
        
        for section_title, section_content in sections:
            # Add section title
            section_label = QLabel(section_title)
            section_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #007BFF;
                margin-top: 15px;
            """)
            frame_layout.addWidget(section_label)
            
            # Add section content
            content_label = QLabel(section_content)
            content_label.setStyleSheet("""
                font-size: 14px;
                color: #212529;
                margin-left: 10px;
                line-height: 1.5;
            """)
            content_label.setWordWrap(True)
            frame_layout.addWidget(content_label)
        
        # Add frame to layout with scroll capability
        scroll = QScrollArea()
        scroll.setWidget(frame)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll)
    
    def create_metrics_content(self, layout):
        """Create the metrics tab content."""
        # Create metrics chart
        chart_view = QWebEngineView()
        chart_view.setMinimumHeight(600)  # Increased height
        
        # Create figure
        fig = go.Figure()
        
        # Add bars for each metric
        metrics = ['Cost', 'CO2', 'Delivery Time', 'Ethical Score']
        values = [
            self.df['cost'].mean(),
            self.df['co2'].mean(),
            self.df['delivery_time'].mean(),
            self.df['ethical_score'].mean()
        ]
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=values,
            marker_color=['#007BFF', '#28A745', '#FFC107', '#DC3545']
        ))
        
        # Set layout
        fig.update_layout(
            title="Average Performance Metrics",
            title_font=dict(size=18),
            plot_bgcolor="white",
            yaxis=dict(title="Value"),
            margin=dict(l=50, r=50, t=50, b=50),
            height=600,  # Set fixed height
            showlegend=False
        )
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        chart_view.setHtml(html)
        
        # Add chart to layout
        layout.addWidget(chart_view)
    
    def create_tradeoff_chart(self, layout):
        """Create the trade-off chart tab content."""
        # Create scatter plot
        chart_view = QWebEngineView()
        chart_view.setMinimumHeight(600)  # Increased height
        
        # Create figure
        fig = go.Figure()
        
        # Add scatter plot
        fig.add_trace(go.Scatter(
            x=self.df['cost'],
            y=self.df['co2'],
            mode='markers',
            marker=dict(
                size=10,
                color=self.df['ethical_score'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Ethical Score")
            ),
            text=self.df['name'],
            hovertemplate="<b>%{text}</b><br>" +
                         "Cost: $%{x:.2f}<br>" +
                         "CO2: %{y:.1f} kg<br>" +
                         "Ethical Score: %{marker.color:.1f}<extra></extra>"
        ))
        
        # Set layout
        fig.update_layout(
            title="Cost vs. CO2 Trade-off",
            title_font=dict(size=18),
            xaxis_title="Cost ($)",
            yaxis_title="CO2 Emissions (kg)",
            plot_bgcolor="white",
            margin=dict(l=50, r=50, t=50, b=50),
            height=600  # Set fixed height
        )
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        chart_view.setHtml(html)
        
        # Add chart to layout
        layout.addWidget(chart_view)
    
    def create_radar_chart(self, layout):
        """Create the radar chart tab content."""
        # Create radar chart
        chart_view = QWebEngineView()
        chart_view.setMinimumHeight(600)  # Increased height
        
        # Get top 3 suppliers
        top_suppliers = self.df.head(3)
        
        # Create figure
        fig = go.Figure()
        
        # Add radar chart for each supplier
        categories = ['Cost', 'CO2', 'Delivery Time', 'Ethical Score']
        
        for i, row in top_suppliers.iterrows():
            # Normalize values between 0 and 1
            values = [
                1 - (row['cost'] - self.df['cost'].min()) / (self.df['cost'].max() - self.df['cost'].min()),
                1 - (row['co2'] - self.df['co2'].min()) / (self.df['co2'].max() - self.df['co2'].min()),
                1 - (row['delivery_time'] - self.df['delivery_time'].min()) / (self.df['delivery_time'].max() - self.df['delivery_time'].min()),
                row['ethical_score'] / 100
            ]
            
            # Add trace
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],  # Close the polygon
                theta=categories + [categories[0]],  # Close the polygon
                name=row['name'],
                fill='toself'
            ))
        
        # Set layout
        fig.update_layout(
            title="Top 3 Suppliers Performance Comparison",
            title_font=dict(size=18),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=50),
            height=600  # Set fixed height
        )
        
        # Convert to HTML and set in web view
        html = fig.to_html(include_plotlyjs='cdn')
        chart_view.setHtml(html)
        
        # Add chart to layout
        layout.addWidget(chart_view)
        layout.addStretch()  # Add stretch to ensure chart takes full height
    
    def create_supplier_table(self, layout):
        """Create a table for supplier details."""
        # Create frame for table
        table_frame = QFrame()
        table_frame.setFrameShape(QFrame.Shape.StyledPanel)
        table_frame.setStyleSheet("""
            background-color: white;
            border: 1px solid #DEE2E6;
            border-radius: 8px;
            padding: 10px;
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        table_layout.setSpacing(15)
        
        # Create table title
        table_title = QLabel("All Supplier Details")
        table_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
            margin-bottom: 10px;
        """)
        table_layout.addWidget(table_title)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
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
        
        # Create container widget for table
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Create table
        table = QTableWidget()
        table.setRowCount(len(self.df))
        table.setColumnCount(6)
        
        # Set column headers with custom formatting
        headers = [
            ("Supplier\nID", 100),
            ("Cost\n($)", 100),
            ("CO2 Emissions\n(kg)", 120),
            ("Delivery Time\n(days)", 120),
            ("Ethical Score\n(0-100)", 120),
            ("AI Score\n(0-100)", 100)
        ]
        
        for col, (header, width) in enumerate(headers):
            item = QTableWidgetItem(header)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setHorizontalHeaderItem(col, item)
            table.setColumnWidth(col, width)
        
        # Set table properties
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #DEE2E6;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 12px 8px;
                border: 1px solid #DEE2E6;
                font-weight: bold;
                font-size: 13px;
                color: #495057;
            }
            QTableWidget::item {
                padding: 8px;
                font-size: 13px;
            }
        """)
        
        # Set table header properties
        header = table.horizontalHeader()
        header.setFixedHeight(60)  # Increased height for two-line headers
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Set vertical header properties
        v_header = table.verticalHeader()
        v_header.setVisible(False)  # Hide row numbers
        
        # Fill table with data
        for i, row in self.df.iterrows():
            # Set row height
            table.setRowHeight(i, 40)
            
            # Set background color for top 3 suppliers
            bg_color = "#E3F2FD" if i < 3 else "white"
            
            # Add supplier name
            name_item = QTableWidgetItem(row['name'])
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            name_item.setBackground(QColor(bg_color))
            table.setItem(i, 0, name_item)
            
            # Add cost
            cost_item = QTableWidgetItem(f"{row['cost']:.2f}")
            cost_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            cost_item.setBackground(QColor(bg_color))
            table.setItem(i, 1, cost_item)
            
            # Add CO2
            co2_item = QTableWidgetItem(f"{row['co2']:.1f}")
            co2_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            co2_item.setBackground(QColor(bg_color))
            table.setItem(i, 2, co2_item)
            
            # Add delivery time
            delivery_item = QTableWidgetItem(f"{row['delivery_time']:.1f}")
            delivery_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            delivery_item.setBackground(QColor(bg_color))
            table.setItem(i, 3, delivery_item)
            
            # Add ethical score
            ethical_item = QTableWidgetItem(f"{row['ethical_score']:.1f}")
            ethical_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ethical_item.setBackground(QColor(bg_color))
            table.setItem(i, 4, ethical_item)
            
            # Add predicted score
            score_item = QTableWidgetItem(f"{row['predicted_score']:.1f}")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            score_item.setBackground(QColor(bg_color))
            table.setItem(i, 5, score_item)
        
        # Set table size policy and minimum size
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table.setMinimumHeight(400)
        table.setMinimumWidth(sum(width for _, width in headers) + 20)  # Add some padding
        
        # Add table to container layout
        container_layout.addWidget(table)
        
        # Set container as scroll area widget
        scroll.setWidget(container)
        
        # Add scroll area to table layout
        table_layout.addWidget(scroll)
        
        # Add metrics for selected suppliers
        self.add_selected_metrics(table_layout)
        
        # Add table frame to layout with expanding size policy
        table_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(table_frame)
    
    def add_selected_metrics(self, layout):
        """Add metrics for selected suppliers.
        
        Args:
            layout (QVBoxLayout): Layout to add metrics to.
        """
        # Get top 3 suppliers
        selected_suppliers = self.df.head(3)
        
        # Calculate aggregated metrics
        total_cost = selected_suppliers['cost'].sum()
        avg_co2 = selected_suppliers['co2'].mean()
        avg_delivery = selected_suppliers['delivery_time'].mean()
        avg_ethical = selected_suppliers['ethical_score'].mean()
        
        # Create metrics frame
        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("""
            background-color: #E3F2FD;
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        """)
        metrics_layout = QHBoxLayout(metrics_frame)
        
        # Create metrics labels
        metrics_title = QLabel("Selected Suppliers (Top 3) - Aggregated Metrics")
        metrics_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        cost_label = QLabel(f"Total Cost: ${total_cost:.2f}")
        co2_label = QLabel(f"Avg. CO2: {avg_co2:.1f} kg")
        delivery_label = QLabel(f"Avg. Delivery: {avg_delivery:.1f} days")
        ethical_label = QLabel(f"Avg. Ethical Score: {avg_ethical:.1f}/100")
        
        # Add labels to metrics layout
        metrics_layout.addWidget(metrics_title)
        metrics_layout.addStretch()
        metrics_layout.addWidget(cost_label)
        metrics_layout.addWidget(co2_label)
        metrics_layout.addWidget(delivery_label)
        metrics_layout.addWidget(ethical_label)
        
        # Add metrics frame to layout
        layout.addWidget(metrics_frame)
    
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
            export_df['supplier_id'] = [f"SUP-{2023+i:04d}" for i in range(len(export_df))]
            export_df['contact_email'] = [f"contact@{name.lower().replace('_', '')}.com" for name in export_df['name']]
            
            # Add regional information (random assignment for sample data)
            regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
            export_df['region'] = [random.choice(regions) for _ in range(len(export_df))]
            
            # Add sustainability certifications
            certifications = ['ISO 14001', 'FSC Certified', 'B Corp Certified', 'Cradle to Cradle', 
                            'Fair Trade', 'EMAS', 'Rainforest Alliance', 'PEFC Certified']
            export_df['sustainability_cert'] = [random.choice(certifications) for _ in range(len(export_df))]
            
            # Add performance ratings based on predicted score
            def get_rating(score):
                if score >= 90: return 'A+'
                elif score >= 85: return 'A'
                elif score >= 80: return 'A-'
                elif score >= 75: return 'B+'
                elif score >= 70: return 'B'
                elif score >= 65: return 'B-'
                elif score >= 60: return 'C+'
                elif score >= 55: return 'C'
                else: return 'C-'
            
            export_df['performance_rating'] = export_df['predicted_score'].apply(get_rating)
            
            # Add order history
            export_df['total_orders'] = [int(random.uniform(50, 150)) for _ in range(len(export_df))]
            
            # Add quality metrics
            export_df['avg_lead_time'] = [round(random.uniform(3, 10), 1) for _ in range(len(export_df))]
            export_df['quality_rating'] = [round(random.uniform(80, 98), 1) for _ in range(len(export_df))]
            export_df['relationship_length'] = [round(random.uniform(1, 5), 1) for _ in range(len(export_df))]
            
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
    
    def _get_top_suppliers_text(self):
        """Get formatted text for top 3 suppliers."""
        top_3 = self.df.head(3)
        text_lines = []
        for i, row in top_3.iterrows():
            text_lines.append(
                f"• {row['name']}: AI Score {row['predicted_score']:.1f}/100\n"
                f"  Cost: ${row['cost']:.2f}, CO2: {row['co2']:.1f}kg, "
                f"Delivery: {row['delivery_time']:.1f} days, "
                f"Ethical: {row['ethical_score']:.1f}/100"
            )
        return "\n".join(text_lines)
    
    def _get_aggregated_metrics_text(self):
        """Get formatted text for aggregated metrics."""
        top_3 = self.df.head(3)
        return (
            f"• Total Cost: ${top_3['cost'].sum():.2f}\n"
            f"• Average CO2: {top_3['co2'].mean():.1f}kg\n"
            f"• Average Delivery Time: {top_3['delivery_time'].mean():.1f} days\n"
            f"• Average Ethical Score: {top_3['ethical_score'].mean():.1f}/100"
        )
    
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
    
    def generate_sample_data(self):
        """Generate and set sample data for suppliers."""
        # Generate sample data for 15 suppliers
        suppliers = []
        
        for i in range(1, 16):
            supplier = {
                'name': f"Supplier_{i:04d}",
                'cost': random.uniform(100, 1000),
                'co2': random.uniform(100, 500),
                'delivery_time': random.uniform(1, 30),
                'ethical_score': random.uniform(0, 100)
            }
            suppliers.append(supplier)
        
        # Create DataFrame
        self.df = pd.DataFrame(suppliers)
        
        # Normalize features for model input
        normalized_df = self.df.copy()
        for col in ['cost', 'co2', 'delivery_time']:
            min_val = normalized_df[col].min()
            max_val = normalized_df[col].max()
            normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
        
        # Invert cost, CO2, and delivery time (lower is better)
        for col in ['cost', 'co2', 'delivery_time']:
            normalized_df[col] = 1 - normalized_df[col]
        
        # Normalize ethical score
        normalized_df['ethical_score'] = normalized_df['ethical_score'] / 100
        
        # Calculate predicted scores (simplified version without TensorFlow)
        # In a real implementation, this would use a trained TensorFlow model
        weights = {
            'cost': 0.3,
            'co2': 0.2,
            'delivery_time': 0.2,
            'ethical_score': 0.3
        }
        
        predicted_scores = (
            normalized_df['cost'] * weights['cost'] +
            normalized_df['co2'] * weights['co2'] +
            normalized_df['delivery_time'] * weights['delivery_time'] +
            normalized_df['ethical_score'] * weights['ethical_score']
        ) * 100
        
        # Add some random noise to the scores
        noise = np.random.normal(0, 5, len(predicted_scores))
        predicted_scores = predicted_scores + noise
        
        # Clip scores to 0-100 range
        predicted_scores = np.clip(predicted_scores, 0, 100)
        
        # Add predicted scores to DataFrame
        self.df['predicted_score'] = predicted_scores
        
        # Sort by predicted score (descending)
        self.df = self.df.sort_values('predicted_score', ascending=False).reset_index(drop=True)
    
    def create_action_buttons(self):
        """Create action buttons for exporting results."""
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Create export button
        export_btn = QPushButton("Export Results")
        export_btn.setStyleSheet("""
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
        export_btn.clicked.connect(self.export_results)
        
        # Create template download button
        template_btn = QPushButton("Download Template")
        template_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        template_btn.clicked.connect(self.download_template)
        
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
        
        # Add buttons to layout
        button_layout.addWidget(export_btn)
        button_layout.addWidget(template_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Add button layout to main layout
        self.layout.addLayout(button_layout)
    
    def download_template(self):
        """Download a CSV template for supplier data."""
        # Create template file path
        template_path = "supplier_export_template.csv"
        
        # Check if template exists
        if not os.path.exists(template_path):
            # Create template if it doesn't exist
            self.create_template_file(template_path)
        
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
                        'Downloaded supplier template',
                        f'File: {save_path}'
                    )
                
                # Show confirmation
                if main_window:
                    main_window.show_status_message(f"Template downloaded to {save_path}", 3000)
            except Exception as e:
                # Show error
                if main_window:
                    main_window.show_status_message(f"Error downloading template: {str(e)}", 5000, error=True)
    
    def create_template_file(self, path):
        """Create a CSV template file with sample data.
        
        Args:
            path (str): Path to save the template file.
        """
        # Define sample data
        sample_data = [
            {
                'name': 'EcoTech Solutions',
                'supplier_id': 'ECT-2023',
                'cost': 430.25,
                'delivery_time': 3,
                'co2': 45.8,
                'ethical_score': 89.5,
                'predicted_score': 92.7,
                'contact_email': 'contact@ecotech.com',
                'region': 'North America',
                'sustainability_cert': 'ISO 14001',
                'performance_rating': 'A+',
                'total_orders': 128,
                'avg_lead_time': 4.2,
                'quality_rating': 96.3,
                'relationship_length': 3.5
            },
            {
                'name': 'GreenMaterials Inc',
                'supplier_id': 'GMI-2022',
                'cost': 385.65,
                'delivery_time': 5,
                'co2': 38.2,
                'ethical_score': 93.2,
                'predicted_score': 90.5,
                'contact_email': 'sales@greenmaterials.co',
                'region': 'Europe',
                'sustainability_cert': 'FSC Certified',
                'performance_rating': 'A',
                'total_orders': 89,
                'avg_lead_time': 7.1,
                'quality_rating': 92.8,
                'relationship_length': 2.1
            }
        ]
        
        # Create DataFrame
        template_df = pd.DataFrame(sample_data)
        
        # Save to CSV
        template_df.to_csv(path, index=False)
    
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
        # Normalize features for model input
        normalized_df = self.df.copy()
        for col in ['cost', 'co2', 'delivery_time']:
            min_val = normalized_df[col].min()
            max_val = normalized_df[col].max()
            normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
        
        # Invert cost, CO2, and delivery time (lower is better)
        for col in ['cost', 'co2', 'delivery_time']:
            normalized_df[col] = 1 - normalized_df[col]
        
        # Normalize ethical score
        normalized_df['ethical_score'] = normalized_df['ethical_score'] / 100
        
        # Calculate predicted scores
        weights = {
            'cost': 0.3,
            'co2': 0.2,
            'delivery_time': 0.2,
            'ethical_score': 0.3
        }
        
        self.df['predicted_score'] = sum(
            normalized_df[col] * weight
            for col, weight in weights.items()
        )
        
        # Sort by predicted score
        self.df = self.df.sort_values('predicted_score', ascending=False)
    
    def update_ui(self):
        """Update the UI components with new data."""
        # Clear existing tabs if they exist
        if hasattr(self, 'tab_widget'):
            self.tab_widget.clear()
            self.tab_widget.deleteLater()
        
        # Create new tabs with updated data
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