#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing EthicSupply...${NC}"

# Get the absolute path of the current directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

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
cat > ~/Desktop/EthicSupply.command << EOL
#!/bin/bash
cd "${APP_DIR}"
source venv/bin/activate
python3 run.py
EOL
chmod +x ~/Desktop/EthicSupply.command

# Create Applications folder shortcut
echo -e "${BLUE}Creating Applications shortcut...${NC}"
cat > /Applications/EthicSupply.command << EOL
#!/bin/bash
cd "${APP_DIR}"
source venv/bin/activate
python3 run.py
EOL
chmod +x /Applications/EthicSupply.command

# Create an app bundle
echo -e "${BLUE}Creating application bundle...${NC}"
mkdir -p EthicSupply.app/Contents/MacOS
mkdir -p EthicSupply.app/Contents/Resources

# Create Info.plist
cat > EthicSupply.app/Contents/Info.plist << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>EthicSupply</string>
    <key>CFBundleIdentifier</key>
    <string>com.ethicsupply.app</string>
    <key>CFBundleName</key>
    <string>EthicSupply</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.business</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon.icns</string>
</dict>
</plist>
EOL

# Create the main script
cat > EthicSupply.app/Contents/MacOS/EthicSupply << EOL
#!/bin/bash
cd "${APP_DIR}"
source venv/bin/activate
python3 run.py
EOL
chmod +x EthicSupply.app/Contents/MacOS/EthicSupply

# Create a wrapper script to handle environment variables
cat > EthicSupply.app/Contents/MacOS/run.sh << EOL
#!/bin/bash
export PATH="${APP_DIR}/venv/bin:$PATH"
export PYTHONPATH="${APP_DIR}:$PYTHONPATH"
cd "${APP_DIR}"
source venv/bin/activate
python3 run.py
EOL
chmod +x EthicSupply.app/Contents/MacOS/run.sh

# Update the main executable to use the wrapper
cat > EthicSupply.app/Contents/MacOS/EthicSupply << EOL
#!/bin/bash
"${APP_DIR}/EthicSupply.app/Contents/MacOS/run.sh"
EOL
chmod +x EthicSupply.app/Contents/MacOS/EthicSupply

# Set proper permissions
chmod -R 755 EthicSupply.app
chmod -R 644 EthicSupply.app/Contents/Info.plist

# Move the app bundle to Applications
mv EthicSupply.app /Applications/

echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "You can now launch EthicSupply from:"
echo -e "1. Applications folder (EthicSupply.app)"
echo -e "2. Desktop shortcut"
echo -e "3. Terminal by typing 'python3 run.py'" 