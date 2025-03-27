#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing EthicSupply...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
    echo -e "${RED}Python 3.8 or higher is required. Current version: $PYTHON_VERSION${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install PyQt6>=6.4.0 pandas>=1.5.0 numpy>=1.21.0 plotly>=5.13.0 tensorflow>=2.12.0 scikit-learn>=1.0.0

# Create desktop shortcut
echo -e "${BLUE}Creating desktop shortcut...${NC}"
cat > ~/Desktop/EthicSupply.command << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 run.py
EOL
chmod +x ~/Desktop/EthicSupply.command

# Create Applications folder shortcut
echo -e "${BLUE}Creating Applications shortcut...${NC}"
cat > /Applications/EthicSupply.command << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 run.py
EOL
chmod +x /Applications/EthicSupply.command

echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "You can now launch EthicSupply from:"
echo -e "1. Desktop shortcut"
echo -e "2. Applications folder"
echo -e "3. Terminal by typing 'python3 run.py'" 