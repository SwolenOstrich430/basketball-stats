#!bin/bash

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
    echo "Error: python is not installed or not found in your PATH."
    exit 1 
fi

echo "Checking if Virtual Env Running"
if command echo $VIRTUAL_ENV | grep basketball-stats/.venv &> /dev/null; then
    echo "Virtual environment already running."
else 
    echo "Virtual environmeny not setup. Attempting to create..."
    python3 -m venv .venv
    source .venv/bin/activate
fi 