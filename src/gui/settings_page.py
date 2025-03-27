#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QSpinBox, QDoubleSpinBox,
    QFormLayout, QCheckBox, QComboBox, QMainWindow,
    QScrollArea, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SettingsPage(QWidget):
    """Settings page for configuring application parameters."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Add page title
        title_label = QLabel("Settings")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
        """)
        self.layout.addWidget(title_label)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        # Create container for settings
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Add supplier settings group
        self.create_supplier_settings(container_layout)
        
        # Add optimization settings group
        self.create_optimization_settings(container_layout)
        
        # Add UI settings group
        self.create_ui_settings(container_layout)
        
        # Set container as scroll area widget
        scroll.setWidget(container)
        
        # Add scroll area to main layout
        self.layout.addWidget(scroll)
        
        # Create action buttons
        self.create_action_buttons()
    
    def create_supplier_settings(self, parent_layout):
        """Create supplier-related settings group."""
        group = QGroupBox("Supplier Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #212529;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        
        # Number of suppliers
        self.num_suppliers = QSpinBox()
        self.num_suppliers.setRange(1, 100)
        self.num_suppliers.setValue(5)
        self.num_suppliers.setStyleSheet("padding: 5px;")
        layout.addRow("Default Number of Suppliers:", self.num_suppliers)
        
        # Cost range
        cost_layout = QHBoxLayout()
        self.min_cost = QDoubleSpinBox()
        self.min_cost.setRange(0, 10000)
        self.min_cost.setValue(100)
        self.min_cost.setPrefix("$")
        self.max_cost = QDoubleSpinBox()
        self.max_cost.setRange(0, 10000)
        self.max_cost.setValue(1000)
        self.max_cost.setPrefix("$")
        cost_layout.addWidget(self.min_cost)
        cost_layout.addWidget(QLabel("-"))
        cost_layout.addWidget(self.max_cost)
        layout.addRow("Cost Range:", cost_layout)
        
        parent_layout.addWidget(group)
    
    def create_optimization_settings(self, parent_layout):
        """Create optimization-related settings group."""
        group = QGroupBox("Optimization Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #212529;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        
        # Weights
        self.cost_weight = QDoubleSpinBox()
        self.cost_weight.setRange(0, 1)
        self.cost_weight.setSingleStep(0.1)
        self.cost_weight.setValue(0.3)
        layout.addRow("Cost Weight:", self.cost_weight)
        
        self.co2_weight = QDoubleSpinBox()
        self.co2_weight.setRange(0, 1)
        self.co2_weight.setSingleStep(0.1)
        self.co2_weight.setValue(0.2)
        layout.addRow("CO2 Weight:", self.co2_weight)
        
        self.delivery_weight = QDoubleSpinBox()
        self.delivery_weight.setRange(0, 1)
        self.delivery_weight.setSingleStep(0.1)
        self.delivery_weight.setValue(0.2)
        layout.addRow("Delivery Time Weight:", self.delivery_weight)
        
        self.ethical_weight = QDoubleSpinBox()
        self.ethical_weight.setRange(0, 1)
        self.ethical_weight.setSingleStep(0.1)
        self.ethical_weight.setValue(0.3)
        layout.addRow("Ethical Score Weight:", self.ethical_weight)
        
        # Minimum ethical score
        self.min_ethical = QDoubleSpinBox()
        self.min_ethical.setRange(0, 100)
        self.min_ethical.setValue(50)
        self.min_ethical.setSuffix("/100")
        layout.addRow("Minimum Ethical Score:", self.min_ethical)
        
        parent_layout.addWidget(group)
    
    def create_ui_settings(self, parent_layout):
        """Create UI-related settings group."""
        group = QGroupBox("UI Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #212529;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        
        # Theme selection
        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark"])
        layout.addRow("Theme:", self.theme)
        
        # Auto-save
        self.auto_save = QCheckBox()
        self.auto_save.setChecked(True)
        layout.addRow("Auto-save Results:", self.auto_save)
        
        parent_layout.addWidget(group)
    
    def create_action_buttons(self):
        """Create action buttons."""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_settings)
        
        # Reset button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setStyleSheet("""
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
        reset_btn.clicked.connect(self.reset_settings)
        
        # Add buttons to layout
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        
        # Add button layout to main layout
        self.layout.addLayout(button_layout)
    
    def get_main_window(self):
        """Get the main window from the parent widgets."""
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent
    
    def save_settings(self):
        """Save the current settings."""
        # TODO: Implement settings save functionality
        main_window = self.get_main_window()
        if main_window:
            main_window.show_status_message("Settings saved successfully", 3000)
    
    def reset_settings(self):
        """Reset settings to default values."""
        # Reset supplier settings
        self.num_suppliers.setValue(5)
        self.min_cost.setValue(100)
        self.max_cost.setValue(1000)
        
        # Reset optimization settings
        self.cost_weight.setValue(0.3)
        self.co2_weight.setValue(0.2)
        self.delivery_weight.setValue(0.2)
        self.ethical_weight.setValue(0.3)
        self.min_ethical.setValue(50)
        
        # Reset UI settings
        self.theme.setCurrentText("Light")
        self.auto_save.setChecked(True)
        
        # Show confirmation
        main_window = self.get_main_window()
        if main_window:
            main_window.show_status_message("Settings reset to defaults", 3000) 