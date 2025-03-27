# EthicSupply Documentation

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [User Interface](#user-interface)
6. [Database](#database)
7. [Optimization Model](#optimization-model)
8. [Installation and Setup](#installation-and-setup)
9. [Usage Guide](#usage-guide)
10. [Development Guide](#development-guide)

## Overview

EthicSupply is a supplier optimization application that helps businesses make ethical and efficient supplier decisions. The application uses a multi-criteria decision-making approach to evaluate suppliers based on cost, CO2 emissions, delivery time, and ethical scores.

## Project Structure

```
supply/
├── src/
│   ├── gui/                 # GUI components
│   ├── data/                # Data handling and database
│   ├── models/              # ML models and optimization
│   └── utils/               # Utility functions
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
└── run.py                  # Application entry point
```

## Core Components

### 1. GUI Components (`src/gui/`)

#### MainWindow (`main_window.py`)

- Central application window
- Manages page navigation
- Handles application state
- Coordinates between different components

#### DashboardPage (`dashboard_page.py`)

- Displays key metrics and performance indicators
- Shows optimization trends
- Provides quick access to main features
- Displays recent activity summary

#### InputPage (`input_page.py`)

- Handles supplier data input
- Validates input data
- Manages supplier forms
- Processes data for optimization

#### ResultsPage (`results_page.py`)

- Displays optimization results
- Shows supplier rankings
- Provides detailed supplier comparisons
- Visualizes data through charts and tables

#### Sidebar (`sidebar.py`)

- Provides navigation between pages
- Shows current page status
- Manages user interface state

#### RecentActivityPage (`recent_activity_page.py`)

- Tracks and displays recent actions
- Shows optimization history
- Provides activity details
- Links to related optimizations

### 2. Data Management (`src/data/`)

#### Database (`database.py`)

- Manages data persistence
- Handles data operations
- Provides data access methods
- Maintains data integrity

#### Data Processing (`data_processor.py`)

- Processes raw input data
- Normalizes data for optimization
- Handles data validation
- Prepares data for visualization

### 3. Optimization Model (`src/models/`)

#### Optimization Engine (`optimization_engine.py`)

- Implements optimization algorithms
- Calculates supplier scores
- Handles multi-criteria decision making
- Generates optimization results

## Data Flow

1. **Data Input**

   - User enters supplier data through InputPage
   - Data is validated and processed
   - Processed data is stored in database

2. **Optimization Process**

   - Data is retrieved from database
   - Optimization engine processes data
   - Results are calculated and normalized
   - Results are stored for display

3. **Results Display**
   - Results are retrieved from storage
   - Data is formatted for visualization
   - Charts and tables are generated
   - Results are displayed to user

## User Interface

### Navigation

- Sidebar provides main navigation
- Pages are organized hierarchically
- Current page is highlighted
- Back navigation is available

### Data Input

- Form-based input interface
- Real-time validation
- Error handling and feedback
- Data persistence

### Results Display

- Tabbed interface for different views
- Interactive charts and graphs
- Detailed supplier information
- Export capabilities

## Database

### Schema

- Suppliers table
- Optimization results table
- Activity log table
- Settings table

### Operations

- CRUD operations for suppliers
- Result storage and retrieval
- Activity logging
- Settings management

## Optimization Model

### Scoring System

- Cost evaluation (30%)
- CO2 emissions (25%)
- Delivery time (25%)
- Ethical score (20%)

### Normalization

- Min-max normalization for numerical values
- Inversion for cost, CO2, and delivery time
- Direct normalization for ethical scores

### Visualization

- Radar charts for supplier comparison
- Bar charts for rankings
- Line charts for trends
- Tables for detailed data

## Installation and Setup

### Requirements

- Python 3.8+
- PyQt6
- Pandas
- Plotly
- SQLite3

### Installation Steps

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python run.py`

## Usage Guide

### Starting the Application

1. Launch the application
2. Navigate to Input page
3. Enter supplier data
4. Submit for optimization
5. View results

### Working with Results

1. View supplier rankings
2. Compare suppliers
3. Analyze trends
4. Export data

### Managing Data

1. Add new suppliers
2. Update existing data
3. Delete suppliers
4. Export/Import data

## Development Guide

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

### Adding Features

1. Create new components
2. Update database schema
3. Modify optimization model
4. Update UI

### Testing

- Unit tests for components
- Integration tests for workflows
- UI tests for interface
- Performance testing

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
