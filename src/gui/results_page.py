#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QFileDialog, QMainWindow, QScrollArea, QSpinBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView

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
    
    def create_explanation_content(self, layout):
        """Create the explanation tab content."""
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
        title = QLabel("Supplier Selection Analysis")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #212529;
            margin-bottom: 10px;
        """)
        frame_layout.addWidget(title)
        
        # Add sections
        sections = [
            ("Selection Methodology", """
            Our AI-driven supplier selection process uses a comprehensive multi-criteria approach that balances:
            
            • Cost Efficiency (30%): Prioritizing competitive pricing while ensuring value
            • Environmental Impact (20%): CO2 emissions and sustainability metrics
            • Delivery Performance (20%): Optimizing supply chain speed and reliability
            • Ethical Standards (30%): Ensuring fair labor practices and corporate responsibility
            """),
            
            ("Why These Suppliers?", self._get_supplier_analysis()),
            
            ("Performance Breakdown", f"""
            Top 3 Selected Suppliers Performance:
            {self._get_top_suppliers_text()}
            
            Aggregated Impact:
            {self._get_aggregated_metrics_text()}
            """),
            
            ("Strategic Benefits", """
            The selected combination of suppliers offers several strategic advantages:
            
            • Balanced Cost Structure: Optimal mix of cost-effective suppliers without compromising quality
            • Environmental Responsibility: Combined CO2 footprint below industry average
            • Reliable Delivery: Consistent delivery times with minimal variance
            • Strong Ethical Foundation: All selected suppliers exceed ethical score requirements
            """),
            
            ("Risk Mitigation", """
            Key risk mitigation factors in this selection:
            
            • Supplier Diversity: Different geographical and operational capabilities
            • Performance History: Consistent track record in quality and delivery
            • Ethical Compliance: Strong commitment to sustainable and ethical practices
            • Financial Stability: Robust financial indicators and market position
            """),
            
            ("Recommendations", """
            To maximize the benefits of this selection:
            
            • Implement regular performance monitoring and feedback systems
            • Establish clear communication channels with each supplier
            • Develop contingency plans for supply chain disruptions
            • Schedule quarterly reviews of sustainability metrics
            • Maintain documentation of ethical compliance and certifications
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
    
    def export_results(self):
        """Export the results to a CSV file."""
        # Open file dialog
        options = QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "CSV Files (*.csv)", options=options
        )
        
        if file_name:
            # Add .csv extension if not present
            if not file_name.endswith('.csv'):
                file_name += '.csv'
            
            # Export DataFrame to CSV
            self.df.to_csv(file_name, index=False)
            
            # Show success message in status bar
            main_window = self.get_main_window()
            if main_window:
                main_window.statusBar().showMessage(f"Results exported to {file_name}", 5000)
    
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
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Add button layout to main layout
        self.layout.addLayout(button_layout)
    
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
        """Update the results page with new supplier data.
        
        Args:
            suppliers_data (list): List of supplier dictionaries.
        """
        # Clear existing tabs if they exist
        if hasattr(self, 'tab_widget'):
            self.tab_widget.clear()
            self.tab_widget.deleteLater()
        
        # Create DataFrame from supplier data
        self.df = pd.DataFrame(suppliers_data)
        
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
        
        # Calculate weighted scores
        self.df['predicted_score'] = (
            normalized_df['cost'] * weights['cost'] +
            normalized_df['co2'] * weights['co2'] +
            normalized_df['delivery_time'] * weights['delivery_time'] +
            normalized_df['ethical_score'] * weights['ethical_score']
        ) * 100
        
        # Sort by predicted score
        self.df = self.df.sort_values('predicted_score', ascending=False)
        
        # Create new tabs with updated data
        self.setup_tabs() 