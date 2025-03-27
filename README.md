# EthicSupply - Ethical AI Supply Chain Optimizer

A Python-based application that uses machine learning to optimize supply chain decisions while considering ethical and sustainability factors.

## Features

- ML-powered supplier selection
- Ethical constraints and fairness metrics
- Sustainability optimization
- Cost and delivery time efficiency
- Interactive visualizations
- User-friendly GUI

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Method 1: Install from PyPI (Recommended)

```bash
pip install ethicsupply
```

### Method 2: Install from Source

1. Clone the repository:

```bash
git clone https://github.com/ne3mer/ethicsupply.git
cd ethicsupply
```

2. Install the package:

```bash
pip install -e .
```

### Method 3: Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/ne3mer/ethicsupply.git
cd ethicsupply
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

After installation, you can run the application in one of two ways:

1. Using the command-line entry point:

```bash
ethicsupply
```

2. Running the main script directly:

```bash
python run.py
```

## Project Structure

```
ethicsupply/
├── src/
│   ├── gui/           # GUI components
│   ├── ml/            # Machine learning models
│   ├── utils/         # Utility functions
│   └── data/          # Data processing
├── tests/             # Test files
├── docs/              # Documentation
├── setup.py           # Package setup file
├── requirements.txt   # Project dependencies
├── README.md         # Project documentation
└── LICENSE           # MIT License
```

## Development

To set up the development environment:

1. Clone the repository:

```bash
git clone https://github.com/ne3mer/ethicsupply.git
cd ethicsupply
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Mohammad Afsharfar
- Supervisor: Dr. Alpár Vera Noémi

## Acknowledgments

- Special thanks to all contributors and supporters
- Built with PyQt6 and TensorFlow
