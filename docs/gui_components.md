# GUI Components Documentation

## MainWindow (`src/gui/main_window.py`)

### Overview

The MainWindow class serves as the central container for the application. It manages the overall layout, navigation between pages, and application state.

### Key Components

1. **Layout Structure**

   ```python
   self.setLayout(QHBoxLayout())
   self.layout().setContentsMargins(0, 0, 0, 0)
   self.layout().setSpacing(0)
   ```

   - Uses horizontal layout for sidebar and content area
   - Removes margins and spacing for full-window appearance

2. **Page Management**

   ```python
   self.pages = {
       'dashboard': DashboardPage(self),
       'input': InputPage(self),
       'results': ResultsPage(self),
       'recent_activity': RecentActivityPage(self),
       'settings': SettingsPage(self),
       'about': AboutPage(self)
   }
   ```

   - Maintains dictionary of all application pages
   - Handles page instantiation and navigation

3. **Navigation System**
   ```python
   def navigate_to(self, page_name):
       if page_name in self.pages:
           self.content_area.setCurrentWidget(self.pages[page_name])
   ```
   - Manages page switching
   - Updates status bar with current page
   - Handles navigation state

## DashboardPage (`src/gui/dashboard_page.py`)

### Overview

The DashboardPage provides an overview of the application's key metrics and quick access to main features.

### Key Features

1. **Performance Overview**

   - Displays key metrics in card format
   - Shows optimization trends
   - Provides quick statistics

2. **Quick Actions**

   - Start new optimization
   - Load existing data
   - Load sample data
   - Export results

3. **Layout Structure**
   ```python
   self.setLayout(QVBoxLayout())
   self.layout().setContentsMargins(20, 20, 20, 20)
   ```
   - Vertical layout with proper margins
   - Organized sections for different components

## InputPage (`src/gui/input_page.py`)

### Overview

The InputPage handles supplier data input and validation.

### Key Features

1. **Supplier Form**

   - Dynamic form creation
   - Input validation
   - Data collection

2. **Form Management**

   ```python
   def add_supplier_form(self):
       form = SupplierForm()
       self.forms.append(form)
       self.forms_layout.addWidget(form)
   ```

   - Adds new supplier forms
   - Manages form collection
   - Handles form removal

3. **Data Processing**
   ```python
   def submit_data(self):
       suppliers_data = []
       for form in self.forms:
           data = form.get_data()
           if data:
               suppliers_data.append(data)
   ```
   - Collects form data
   - Validates input
   - Processes for optimization

## ResultsPage (`src/gui/results_page.py`)

### Overview

The ResultsPage displays optimization results and supplier comparisons.

### Key Features

1. **Tab Management**

   ```python
   self.tab_widget = QTabWidget()
   self.tab_widget.setStyleSheet("""
       QTabWidget::pane {
           border: 1px solid #DEE2E6;
           border-radius: 8px;
           background: white;
       }
   """)
   ```

   - Creates tabbed interface
   - Manages different views
   - Handles tab switching

2. **Visualization Components**

   - Radar charts for supplier comparison
   - Bar charts for rankings
   - Tables for detailed data

3. **Data Display**
   ```python
   def update_results(self, suppliers_data):
       self.df = pd.DataFrame(suppliers_data)
       self.setup_tabs()
   ```
   - Updates display with new data
   - Refreshes all visualizations
   - Maintains data consistency

## Sidebar (`src/gui/sidebar.py`)

### Overview

The Sidebar provides navigation and status information.

### Key Features

1. **Navigation Buttons**

   ```python
   self.nav_buttons = {
       'dashboard': self.create_nav_button('Dashboard', 'dashboard'),
       'input': self.create_nav_button('Input', 'input'),
       'results': self.create_nav_button('Results', 'results'),
       'recent_activity': self.create_nav_button('Recent Activity', 'recent_activity'),
       'settings': self.create_nav_button('Settings', 'settings'),
       'about': self.create_nav_button('About', 'about')
   }
   ```

   - Creates navigation buttons
   - Manages button states
   - Handles navigation events

2. **Status Display**
   - Shows current page
   - Indicates active section
   - Provides visual feedback

## RecentActivityPage (`src/gui/recent_activity_page.py`)

### Overview

The RecentActivityPage tracks and displays recent actions.

### Key Features

1. **Activity List**

   ```python
   def add_activity_item(self, description, activity_type='info'):
       item = QFrame()
       item.setFrameShape(QFrame.Shape.StyledPanel)
   ```

   - Creates activity items
   - Manages activity display
   - Handles activity updates

2. **Activity Types**

   - Info: General information
   - Success: Successful operations
   - Warning: Potential issues
   - Error: Error messages

3. **Layout Management**
   ```python
   self.setLayout(QVBoxLayout())
   self.layout().setContentsMargins(20, 20, 20, 20)
   ```
   - Organizes activity items
   - Provides scrollable view
   - Maintains consistent spacing

## Common Features

### Styling

All components use consistent styling:

```python
STYLE_SHEET = """
    QWidget {
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton {
        padding: 8px 16px;
        border-radius: 4px;
        background-color: #007BFF;
        color: white;
        border: none;
    }
    QPushButton:hover {
        background-color: #0056B3;
    }
"""
```

### Error Handling

Components implement error handling:

```python
try:
    # Operation
except Exception as e:
    QMessageBox.critical(self, "Error", str(e))
```

### Data Validation

Input validation is implemented across components:

```python
def validate_input(self):
    if not self.validate_required_fields():
        return False
    if not self.validate_numeric_ranges():
        return False
    return True
```

### Event Handling

Components use Qt's signal/slot mechanism:

```python
button.clicked.connect(self.handle_click)
```

## Best Practices

1. **Component Organization**

   - Keep components modular
   - Use clear naming conventions
   - Implement proper inheritance

2. **Performance**

   - Minimize UI updates
   - Use efficient data structures
   - Implement proper cleanup

3. **User Experience**

   - Provide clear feedback
   - Handle errors gracefully
   - Maintain consistent styling

4. **Code Quality**
   - Follow PEP 8 guidelines
   - Add proper documentation
   - Implement error handling
