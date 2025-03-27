# EthicSupply - Ethical AI Supply Chain Optimizer

EthicSupply is a desktop application that helps optimize supply chain decisions using ethical AI principles. The application balances efficiency, sustainability, and fairness in supplier selection through a TensorFlow-based machine learning model.

## Features

- **AI-Powered Optimization**: Uses machine learning to select optimal suppliers based on multiple criteria
- **Ethical Constraints**: Enforces minimum ethical standards and fairness in supplier selection
- **Interactive GUI**: Modern, user-friendly interface with real-time visualization
- **Data Management**:
  - Import/Export supplier data via CSV
  - Generate sample data for testing
  - Dynamic supplier form management
- **Customizable Settings**:
  - Adjust optimization weights
  - Set minimum ethical standards
  - Configure cost ranges and supplier limits
  - UI preferences

## Screenshots

[Screenshots will be added here]

## Requirements

- Python 3.8+
- PyQt6
- TensorFlow 2.x
- Plotly
- Pandas
- NumPy

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ethicsupply.git
cd ethicsupply
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

## Usage

1. **Input Supplier Data**:

   - Add suppliers manually using the form
   - Generate sample data for testing
   - Import data from CSV
   - Download CSV template for bulk data entry

2. **Configure Settings**:

   - Set optimization weights for different factors
   - Adjust minimum ethical standards
   - Configure cost ranges
   - Set UI preferences

3. **Run Optimization**:

   - Click "Optimize Selection" to run the AI model
   - View results in multiple formats:
     - Supplier rankings
     - Performance metrics
     - Detailed analysis
     - Charts and visualizations

4. **Export Results**:
   - Save optimization results
   - Export supplier data
   - Generate reports

## Project Structure

```
ethicsupply/
├── src/
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── dashboard_page.py
│   │   ├── input_page.py
│   │   ├── results_page.py
│   │   ├── settings_page.py
│   │   └── sidebar.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── supplier_model.py
│   └── utils/
│       └── __init__.py
├── models/
├── data/
├── requirements.txt
├── run.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was developed as part of an MBA thesis on ethical AI in supply chain management
- Special thanks to [Your University/Institution Name] for their support
