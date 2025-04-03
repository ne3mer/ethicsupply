#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import pandas as pd
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox,
    QFormLayout, QScrollArea, QMessageBox, QMainWindow,
    QFileDialog, QGridLayout, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QDoubleValidator, QIntValidator

class SupplierForm(QWidget):
    """Form for supplier data input."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components."""
        # Main layout
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Supplier Information")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title, 0, 0, 1, 2)
        
        # Form fields
        
        # Supplier name
        layout.addWidget(QLabel("Name:"), 1, 0)
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit, 1, 1)
        
        # Supplier ID
        layout.addWidget(QLabel("Supplier ID:"), 2, 0)
        self.supplier_id_edit = QLineEdit()
        layout.addWidget(self.supplier_id_edit, 2, 1)
        
        # Cost
        layout.addWidget(QLabel("Cost ($):"), 3, 0)
        self.cost_edit = QLineEdit()
        self.cost_edit.setValidator(QDoubleValidator(0, 1000000, 2))
        layout.addWidget(self.cost_edit, 3, 1)
        
        # CO2 emissions
        layout.addWidget(QLabel("CO2 Emissions (kg):"), 4, 0)
        self.co2_edit = QLineEdit()
        self.co2_edit.setValidator(QDoubleValidator(0, 1000000, 2))
        layout.addWidget(self.co2_edit, 4, 1)
        
        # Delivery time
        layout.addWidget(QLabel("Delivery Time (days):"), 5, 0)
        self.delivery_time_edit = QLineEdit()
        self.delivery_time_edit.setValidator(QDoubleValidator(1, 365, 2))
        layout.addWidget(self.delivery_time_edit, 5, 1)
        
        # Contact email
        layout.addWidget(QLabel("Contact Email:"), 6, 0)
        self.contact_email_edit = QLineEdit()
        layout.addWidget(self.contact_email_edit, 6, 1)
        
        # Region
        layout.addWidget(QLabel("Region:"), 7, 0)
        self.region_edit = QComboBox()
        self.region_edit.addItems(["North America", "Europe", "Asia", "Africa", "South America", "Australia/Oceania"])
        layout.addWidget(self.region_edit, 7, 1)
        
        # Sustainability certification
        layout.addWidget(QLabel("Sustainability Certification:"), 8, 0)
        self.sustainability_cert_edit = QLineEdit()
        layout.addWidget(self.sustainability_cert_edit, 8, 1)
        
        # Note informing about ethical score calculation
        ethical_note = QLabel("Note: Ethical score will be calculated automatically by the AI model")
        ethical_note.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(ethical_note, 9, 0, 1, 2)
        
        # Stretch at the end
        layout.setRowStretch(10, 1)
    
    def clear(self):
        """Clear all form fields."""
        self.name_edit.clear()
        self.supplier_id_edit.clear()
        self.cost_edit.clear()
        self.co2_edit.clear()
        self.delivery_time_edit.clear()
        self.contact_email_edit.clear()
        self.region_edit.setCurrentIndex(0)
        self.sustainability_cert_edit.clear()
    
    def get_data(self):
        """Get data from the form.
        
        Returns:
            dict: Data from the form
        """
        try:
            return {
                "name": self.name_edit.text() or f"Supplier_{random.randint(1, 100):02d}",
                "cost": float(self.cost_edit.text()) if self.cost_edit.text() else random.uniform(100, 1000),
                "co2": float(self.co2_edit.text()) if self.co2_edit.text() else random.uniform(10, 100),
                "delivery_time": float(self.delivery_time_edit.text()) if self.delivery_time_edit.text() else random.uniform(1, 30),
            }
        except ValueError as e:
            print(f"Error converting form data: {e}")
            return {
                "name": self.name_edit.text() or f"Supplier_{random.randint(1, 100):02d}",
                "cost": random.uniform(100, 1000),
                "co2": random.uniform(10, 100),
                "delivery_time": random.uniform(1, 30),
            }
    
    def set_data(self, data):
        """Set the form data.
        
        Args:
            data (dict): Form data.
        """
        self.name_edit.setText(data.get("name", ""))
        self.supplier_id_edit.setText(data.get("supplier_id", ""))
        self.cost_edit.setText(str(data.get("cost", "")))
        self.co2_edit.setText(str(data.get("co2", "")))
        self.delivery_time_edit.setText(str(data.get("delivery_time", "")))
        self.contact_email_edit.setText(data.get("contact_email", ""))
        
        # Set region if it exists in the combo box
        region = data.get("region", "")
        index = self.region_edit.findText(region)
        if index >= 0:
            self.region_edit.setCurrentIndex(index)
        
        self.sustainability_cert_edit.setText(data.get("sustainability_cert", ""))

class InputPage(QWidget):
    """Page for inputting supplier data."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Add page title
        title_label = QLabel("Input Supplier Data")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #212529;
        """)
        self.layout.addWidget(title_label)
        
        # Create description
        description = QLabel(
            "Enter details for each supplier. The model will optimize the selection "
            "based on cost, delivery time, CO2 emissions, and ethical scores."
        )
        description.setStyleSheet("color: #6C757D;")
        description.setWordWrap(True)
        self.layout.addWidget(description)
        
        # Create data management buttons
        self.create_data_management()
        
        # Create supplier management buttons
        self.create_supplier_management()
        
        # Create scroll area for forms
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        # Create container widget for forms
        self.forms_container = QWidget()
        self.forms_layout = QVBoxLayout(self.forms_container)
        self.forms_layout.setSpacing(20)
        
        # Add forms container to scroll area
        scroll_area.setWidget(self.forms_container)
        self.layout.addWidget(scroll_area)
        
        # Initialize supplier forms list
        self.supplier_forms = []
        
        # Create initial supplier forms (default 5)
        self.create_initial_forms()
        
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Create submit button
        submit_btn = QPushButton("Optimize Selection")
        submit_btn.setStyleSheet("""
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
        submit_btn.clicked.connect(self.submit_data)
        
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
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Add button layout to main layout
        self.layout.addLayout(button_layout)
    
    def create_supplier_management(self):
        """Create buttons for managing supplier forms."""
        management_layout = QHBoxLayout()
        
        # Create add button
        add_btn = QPushButton("Add Supplier")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_btn.clicked.connect(self.add_supplier_form)
        
        # Create remove button
        remove_btn = QPushButton("Remove Last Supplier")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
        """)
        remove_btn.clicked.connect(self.remove_last_supplier)
        
        # Add buttons to layout
        management_layout.addWidget(add_btn)
        management_layout.addWidget(remove_btn)
        management_layout.addStretch()
        
        # Add management layout to main layout
        self.layout.addLayout(management_layout)
    
    def create_initial_forms(self):
        """Create initial supplier forms based on settings."""
        # Create default number of forms first
        num_suppliers = 5  # Default value
        
        for i in range(1, num_suppliers + 1):
            self.add_supplier_form()
        
        # Update settings after initialization
        main_window = self.get_main_window()
        if main_window and hasattr(main_window, 'pages'):
            settings = main_window.pages['settings']
            num_suppliers = settings.num_suppliers.value()
            
            # Adjust number of forms if needed
            while len(self.supplier_forms) < num_suppliers:
                self.add_supplier_form()
            while len(self.supplier_forms) > num_suppliers:
                self.remove_last_supplier()
    
    def add_supplier_form(self):
        """Add a new supplier form."""
        supplier_number = len(self.supplier_forms) + 1
        form = SupplierForm()
        self.supplier_forms.append(form)
        self.forms_layout.addWidget(form)
    
    def remove_last_supplier(self):
        """Remove the last supplier form."""
        if self.supplier_forms:
            # Get the last form
            form = self.supplier_forms.pop()
            
            # Remove from layout
            self.forms_layout.removeWidget(form)
            
            # Delete the widget
            form.deleteLater()
            
            # Update button states - ensure remove button is enabled only when we have more than one form
            self.update_button_states()
            
            # Update minimum height
            self.forms_container.setMinimumHeight(
                max(self.forms_layout.count() * 140, 300)
            )
    
    def get_main_window(self):
        """Get the main window from the parent widgets."""
        parent = self.parent()
        while parent is not None and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        return parent
    
    def back_to_dashboard(self):
        """Navigate back to the dashboard."""
        main_window = self.get_main_window()
        if main_window:
            main_window.navigate_to('dashboard')
    
    def submit_data(self):
        """Submit the supplier data for optimization."""
        # Collect data from all forms
        suppliers_data = [form.get_data() for form in self.supplier_forms]
        
        # Validate data
        for i, supplier in enumerate(suppliers_data):
            if not supplier['name']:
                supplier['name'] = f"Supplier_{i+1:02d}"
            
            # Check for required fields
            required_fields = ['cost', 'co2', 'delivery_time']
            missing_fields = [field for field in required_fields if not supplier.get(field)]
            
            if missing_fields:
                QMessageBox.warning(
                    self,
                    "Missing Data",
                    f"Supplier {supplier['name']} is missing required data: {', '.join(missing_fields)}. "
                    "Please complete all required fields."
                )
                return
        
        # Log activity
        main_window = self.get_main_window()
        if main_window and hasattr(main_window, 'db'):
            main_window.db.log_activity(
                'input',
                f'Submitted data for {len(suppliers_data)} suppliers',
                f'Suppliers: {", ".join(s["name"] for s in suppliers_data)}'
            )
        
        # Update results page with new data
        if main_window and hasattr(main_window, 'pages'):
            main_window.pages['results'].update_results(suppliers_data)
            main_window.navigate_to('results')
    
    def create_data_management(self):
        """Create buttons for data management."""
        management_layout = QHBoxLayout()
        
        # Create generate sample data button
        generate_btn = QPushButton("Generate Sample Data")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #17A2B8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        generate_btn.clicked.connect(self.generate_sample_data)
        
        # Create download template button
        template_btn = QPushButton("Download CSV Template")
        template_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5A6268;
            }
        """)
        template_btn.clicked.connect(self.download_csv_template)
        
        # Create upload CSV button
        upload_btn = QPushButton("Upload CSV Data")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: #212529;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E0A800;
            }
        """)
        upload_btn.clicked.connect(self.upload_csv_data)
        
        # Add buttons to layout
        management_layout.addWidget(generate_btn)
        management_layout.addWidget(template_btn)
        management_layout.addWidget(upload_btn)
        management_layout.addStretch()
        
        # Add management layout to main layout
        self.layout.addLayout(management_layout)
    
    def generate_sample_data(self):
        """Generate sample supplier data."""
        try:
            # Clear existing forms data but keep the forms
            for form in self.supplier_forms:
                form.clear()
            
            # Make sure we have at least 5 forms
            current_forms = len(self.supplier_forms)
            if current_forms < 5:
                for i in range(5 - current_forms):
                    self.add_supplier_form()
            
            # Now populate all forms with sample data
            for i, form in enumerate(self.supplier_forms):
                # Set sample data
                form.name_edit.setText(f"Supplier_{i+1:02d}")
                form.cost_edit.setText(str(round(random.uniform(300, 800), 2)))
                form.co2_edit.setText(str(round(random.uniform(30, 100), 1)))
                form.delivery_time_edit.setText(str(round(random.uniform(3, 25), 1)))
            
            # Log activity
            main_window = self.get_main_window()
            if main_window and hasattr(main_window, 'db'):
                main_window.db.log_activity(
                    'input',
                    'Generated sample data',
                    f'Generated data for {len(self.supplier_forms)} suppliers'
                )
        except Exception as e:
            print(f"Error generating sample data: {e}")
    
    def update_button_states(self):
        """Update the state of add/remove buttons."""
        if hasattr(self, 'remove_btn'):
            self.remove_btn.setEnabled(len(self.supplier_forms) > 1)
    
    def download_csv_template(self):
        """Download a CSV template for supplier data."""
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV Template",
            "supplier_template.csv",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                # Check if the enhanced template exists
                template_path = "supplier_export_template.csv"
                if os.path.exists(template_path):
                    # Copy the enhanced template
                    import shutil
                    shutil.copy(template_path, file_path)
                else:
                    # Fall back to creating a basic template
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['name', 'cost', 'delivery_time', 'co2'])
                        writer.writerow(['Supplier_01', '300', '3', '100'])  # Example row
                
                # Log activity
                main_window = self.get_main_window()
                if main_window and hasattr(main_window, 'db'):
                    main_window.db.log_activity(
                        'export',
                        'Downloaded CSV template',
                        f'File: {file_path}'
                    )
                
                # Show confirmation
                if main_window:
                    main_window.show_status_message("CSV template downloaded successfully", 3000)
            except Exception as e:
                # Show error
                QMessageBox.warning(
                    self,
                    "Template Error",
                    f"Error creating template: {str(e)}"
                )
    
    def upload_csv_data(self):
        """Upload supplier data from a CSV file."""
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload CSV Data",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                # Read CSV file
                suppliers = []
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        suppliers.append(row)
                
                # Clear existing forms
                while self.supplier_forms:
                    self.remove_last_supplier()
                
                # Create new forms with CSV data
                for i, supplier in enumerate(suppliers, 1):
                    self.add_supplier_form()
                    self.supplier_forms[-1].set_data(supplier)
                
                # Show confirmation
                main_window = self.get_main_window()
                if main_window:
                    main_window.show_status_message("CSV data uploaded successfully", 3000)
            
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Upload Error",
                    f"Error uploading CSV data: {str(e)}\n\n"
                    "Please make sure the CSV file has the correct format:\n"
                    "name, cost, delivery_time, co2"
                ) 