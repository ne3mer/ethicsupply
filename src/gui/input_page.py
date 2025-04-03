#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QLineEdit, QSpinBox, QDoubleSpinBox,
    QFormLayout, QScrollArea, QMessageBox, QMainWindow,
    QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SupplierForm(QFrame):
    """Form for inputting supplier data."""
    
    def __init__(self, supplier_number, parent=None):
        super().__init__(parent)
        
        # Store supplier number
        self.supplier_number = supplier_number
        
        # Set frame properties
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DEE2E6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        # Create layout
        layout = QFormLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Create input fields
        self.name = QLineEdit()
        self.name.setPlaceholderText(f"Supplier_{supplier_number:02d}")
        self.cost = QDoubleSpinBox()
        self.cost.setRange(100, 500)
        self.cost.setValue(300)
        self.cost.setPrefix("$")
        self.delivery_time = QSpinBox()
        self.delivery_time.setRange(1, 60)
        self.delivery_time.setValue(5)
        self.delivery_time.setSuffix(" days")
        self.co2 = QDoubleSpinBox()
        self.co2.setRange(50, 200)
        self.co2.setValue(100)
        self.co2.setSuffix(" kg")
        self.ethical_score = QDoubleSpinBox()
        self.ethical_score.setRange(0, 100)
        self.ethical_score.setValue(75)
        self.ethical_score.setSuffix("/100")
        
        # Add fields to layout
        layout.addRow("Supplier Name:", self.name)
        layout.addRow("Cost:", self.cost)
        layout.addRow("Delivery Time:", self.delivery_time)
        layout.addRow("CO2 Emissions:", self.co2)
        layout.addRow("Ethical Score:", self.ethical_score)
    
    def get_data(self):
        """Get the supplier data as a dictionary."""
        return {
            'name': self.name.text() or f"Supplier_{self.supplier_number:02d}",
            'cost': self.cost.value(),
            'delivery_time': self.delivery_time.value(),
            'co2': self.co2.value(),
            'ethical_score': self.ethical_score.value()
        }
    
    def set_data(self, data):
        """Set the form data from a dictionary."""
        self.name.setText(data.get('name', ''))
        self.cost.setValue(float(data.get('cost', 300)))
        self.delivery_time.setValue(int(data.get('delivery_time', 5)))
        self.co2.setValue(float(data.get('co2', 100)))
        self.ethical_score.setValue(float(data.get('ethical_score', 75)))

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
        remove_btn.clicked.connect(self.remove_supplier_form)
        
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
                self.remove_supplier_form()
    
    def add_supplier_form(self):
        """Add a new supplier form."""
        supplier_number = len(self.supplier_forms) + 1
        form = SupplierForm(supplier_number)
        self.supplier_forms.append(form)
        self.forms_layout.addWidget(form)
        
        # Update form ranges based on settings
        main_window = self.get_main_window()
        if main_window and hasattr(main_window, 'pages'):
            settings = main_window.pages['settings']
            form.cost.setRange(settings.min_cost.value(), settings.max_cost.value())
            form.ethical_score.setMinimum(settings.min_ethical.value())
    
    def remove_supplier_form(self):
        """Remove the last supplier form."""
        if len(self.supplier_forms) > 1:  # Keep at least one form
            form = self.supplier_forms.pop()
            form.deleteLater()
            self.forms_layout.removeWidget(form)
    
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
        
        # Get minimum ethical score from settings
        main_window = self.get_main_window()
        min_ethical = 50  # Default value
        if main_window and hasattr(main_window, 'pages'):
            settings = main_window.pages['settings']
            min_ethical = settings.min_ethical.value()
        
        # Validate data
        for supplier in suppliers_data:
            if supplier['ethical_score'] < min_ethical:
                QMessageBox.warning(
                    self,
                    "Invalid Data",
                    f"Supplier {supplier['name']} has an ethical score below {min_ethical}. "
                    "Please adjust the score to meet minimum requirements."
                )
                return
        
        # Log activity
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
        """Generate random sample data for all supplier forms."""
        main_window = self.get_main_window()
        settings = main_window.pages['settings'] if main_window else None
        
        for form in self.supplier_forms:
            # Get ranges from settings if available
            min_cost = settings.min_cost.value() if settings else 100
            max_cost = settings.max_cost.value() if settings else 1000
            min_ethical = settings.min_ethical.value() if settings else 50
            
            # Generate random data
            data = {
                'name': f"Supplier_{form.supplier_number:02d}",
                'cost': random.uniform(min_cost, max_cost),
                'delivery_time': random.randint(1, 30),
                'co2': random.uniform(50, 200),
                'ethical_score': random.uniform(min_ethical, 100)
            }
            
            # Set the data in the form
            form.set_data(data)
        
        # Log activity
        if main_window and hasattr(main_window, 'db'):
            main_window.db.log_activity(
                'input',
                'Generated sample data',
                f'Generated data for {len(self.supplier_forms)} suppliers'
            )
        
        # Show confirmation
        if main_window:
            main_window.show_status_message("Sample data generated successfully", 3000)
    
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
            # Write template file
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'cost', 'delivery_time', 'co2', 'ethical_score'])
                writer.writerow(['Supplier_01', '300', '3', '100', '75'])  # Example row
            
            # Show confirmation
            main_window = self.get_main_window()
            if main_window:
                main_window.show_status_message("CSV template downloaded successfully", 3000)
    
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
                    self.remove_supplier_form()
                
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
                    "name, cost, delivery_time, co2, ethical_score"
                ) 