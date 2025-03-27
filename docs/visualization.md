# Visualization Components Documentation

## Overview

The visualization components in EthicSupply use Plotly for creating interactive charts and graphs. These components are primarily located in the `ResultsPage` class and provide various ways to visualize supplier data and optimization results.

## Chart Types

### 1. Radar Chart (Supplier Comparison)

```python
def create_radar_chart(self, layout):
    chart_view = QWebEngineView()
    chart_view.setMinimumHeight(600)

    # Get top 3 suppliers
    top_suppliers = self.df.head(3)

    # Create figure
    fig = go.Figure()

    # Add radar chart for each supplier
    categories = ['Cost', 'CO2', 'Delivery Time', 'Ethical Score']

    for i, row in top_suppliers.iterrows():
        values = [
            1 - (row['cost'] - self.df['cost'].min()) / (self.df['cost'].max() - self.df['cost'].min()),
            1 - (row['co2'] - self.df['co2'].min()) / (self.df['co2'].max() - self.df['co2'].min()),
            1 - (row['delivery_time'] - self.df['delivery_time'].min()) / (self.df['delivery_time'].max() - self.df['delivery_time'].min()),
            row['ethical_score'] / 100
        ]

        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],  # Close the polygon
            name=row['name'],
            fill='toself'
        ))
```

#### Features

- Compares top 3 suppliers across all metrics
- Normalized values for fair comparison
- Interactive legend
- Filled areas for better visualization
- Responsive sizing

### 2. Bar Chart (Supplier Rankings)

```python
def create_ranking_chart(self, layout):
    chart_view = QWebEngineView()
    chart_view.setMinimumHeight(600)

    # Create figure
    fig = go.Figure()

    # Add bar chart
    fig.add_trace(go.Bar(
        x=self.df['name'],
        y=self.df['predicted_score'],
        text=self.df['predicted_score'].round(2),
        textposition='auto',
        marker_color='#007BFF'
    ))
```

#### Features

- Shows all suppliers ranked by score
- Displays actual score values
- Consistent color scheme
- Interactive tooltips
- Responsive layout

### 3. Line Chart (Optimization Trends)

```python
def create_trend_chart(self, layout):
    chart_view = QWebEngineView()
    chart_view.setMinimumHeight(600)

    # Create figure
    fig = go.Figure()

    # Add line chart
    fig.add_trace(go.Scatter(
        x=self.df.index,
        y=self.df['predicted_score'],
        mode='lines+markers',
        name='Optimization Score'
    ))
```

#### Features

- Shows score progression
- Interactive data points
- Smooth line interpolation
- Clear trend visualization
- Responsive design

## Layout Management

### 1. Tab Organization

```python
def setup_tabs(self):
    self.tab_widget = QTabWidget()
    self.tab_widget.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #DEE2E6;
            border-radius: 8px;
            background: white;
        }
    """)

    # Create tabs
    self.create_ranking_chart(self.tab_widget)
    self.create_supplier_table(self.tab_widget)
    self.create_explanation_tab(self.tab_widget)
    self.create_metrics_tab(self.tab_widget)
    self.create_trade_off_chart(self.tab_widget)
    self.create_radar_chart(self.tab_widget)
```

### 2. Chart Layout

```python
fig.update_layout(
    title="Chart Title",
    title_font=dict(size=18),
    margin=dict(l=50, r=50, t=50, b=50),
    height=600,
    showlegend=True
)
```

## Data Processing for Visualization

### 1. Data Normalization

```python
def normalize_data_for_visualization(self, df):
    # Normalize numerical columns
    for col in ['cost', 'co2', 'delivery_time']:
        df[f'{col}_normalized'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    # Invert normalized values
    for col in ['cost', 'co2', 'delivery_time']:
        df[f'{col}_normalized'] = 1 - df[f'{col}_normalized']
```

### 2. Score Calculation

```python
def calculate_visualization_scores(self, df):
    df['predicted_score'] = (
        df['cost_normalized'] * 0.3 +
        df['co2_normalized'] * 0.25 +
        df['delivery_time_normalized'] * 0.25 +
        df['ethical_score'] / 100 * 0.2
    )
```

## Interactive Features

### 1. Hover Information

```python
fig.update_traces(
    hovertemplate="<b>%{x}</b><br>" +
                  "Score: %{y:.2f}<br>" +
                  "<extra></extra>"
)
```

### 2. Click Events

```python
def handle_chart_click(self, event):
    if event.points:
        point = event.points[0]
        supplier_name = point.x
        self.show_supplier_details(supplier_name)
```

### 3. Zoom and Pan

```python
fig.update_layout(
    dragmode='zoom',
    hovermode='closest',
    showlegend=True
)
```

## Best Practices

### 1. Performance

- Use efficient data structures
- Minimize data transformations
- Implement proper cleanup
- Cache processed data

### 2. User Experience

- Clear labels and titles
- Consistent color schemes
- Intuitive interactions
- Responsive design

### 3. Accessibility

- High contrast colors
- Clear text labels
- Keyboard navigation
- Screen reader support

### 4. Code Organization

- Modular chart creation
- Reusable components
- Clear documentation
- Error handling

## Error Handling

### 1. Data Validation

```python
def validate_visualization_data(self, df):
    required_columns = ['name', 'cost', 'co2', 'delivery_time', 'ethical_score']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
```

### 2. Chart Creation

```python
def create_chart(self, layout):
    try:
        chart_view = QWebEngineView()
        # Create chart
        return chart_view
    except Exception as e:
        logger.error(f"Failed to create chart: {e}")
        raise VisualizationError(f"Chart creation failed: {e}")
```

## Testing

### 1. Unit Tests

```python
def test_chart_creation():
    page = ResultsPage()
    df = create_test_data()
    chart = page.create_radar_chart(df)
    assert chart is not None
    assert chart.height() == 600
```

### 2. Integration Tests

```python
def test_chart_interaction():
    page = ResultsPage()
    df = create_test_data()
    chart = page.create_ranking_chart(df)
    # Simulate user interaction
    event = create_mock_event()
    page.handle_chart_click(event)
    # Verify response
```

### 3. Performance Tests

```python
def test_chart_performance():
    page = ResultsPage()
    df = create_large_dataset()
    start_time = time.time()
    chart = page.create_radar_chart(df)
    duration = time.time() - start_time
    assert duration < 1.0  # Should render within 1 second
```
