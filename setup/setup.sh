#! bin/bash

echo "Updating Homebrew"
brew update;

echo "Checking if Python Installed" 
if command -v python3 &> /dev/null; then
    echo "Python 3 is installed."
else
    echo "Python not installed...installing now"
    brew install python
fi

if ! command -v python3 &> /dev/null
then
    echo "Error: pip is not installed or not found in your PATH."
    echo "Please install pip or ensure it's added to your system's PATH."
    exit 1 # Exit with an error code
fi

echo "Checking if pip Installed" 
if command -v pipx &> /dev/null; then
    echo "pip is installed."
else
    echo "pip is not installed. Attempting to install it..."
    # You can add installation commands here, e.g.:
    brew install pipx
fi

if ! command -v pipx &> /dev/null
then
    echo "Error: pip is not installed or not found in your PATH."
    echo "Please install pip or ensure it's added to your system's PATH."
    exit 1 # Exit with an error code
fi
