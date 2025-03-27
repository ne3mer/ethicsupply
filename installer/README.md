# EthicSupply Installers

This directory contains installation scripts for different operating systems.

## Windows Installation

To create a Windows installer:

1. Install Inno Setup from https://jrsoftware.org/isdl.php
2. Open `installer/windows/installer.iss` in Inno Setup
3. Click "Build" -> "Compile"

The installer will be created in the `dist` directory as `EthicSupply-Setup.exe`.

## Mac Installation

To install on Mac:

1. Open Terminal
2. Navigate to the project directory
3. Run the installation script:

```bash
chmod +x installer/mac/install.sh
./installer/mac/install.sh
```

The script will:

- Check Python requirements
- Create a virtual environment
- Install the package
- Create desktop and Applications folder shortcuts

## Requirements

### Windows

- Windows 10 or higher
- Python 3.8 or higher
- Inno Setup (for creating installer)

### Mac

- macOS 10.15 or higher
- Python 3.8 or higher
- Terminal access
