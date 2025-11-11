#! bin/bash

echo "Updating Homebrew"
brew update;

echo "Checking if Python Installed" 
if command -v python3 &> /dev/null; then
    echo "Python 3 is installed."
else
    echo "Python not installed...installing now"
    brew install python --latest
fi

