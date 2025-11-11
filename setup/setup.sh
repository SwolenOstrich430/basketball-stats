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
    brew install pipx
fi

if ! command -v pipx &> /dev/null
then
    echo "Error: pip is not installed or not found in your PATH."
    echo "Please install pip or ensure it's added to your system's PATH."
    exit 1 
fi

echo "Checking if Flask Installed"
if command pipx list | grep flask &> /dev/null; then
    echo "Flask already installed."
else 
    echo "Flask not installed. Attempting to install it..."
    pipx install Flask
fi 

if ! command pipx list | grep flask &> /dev/null
then
    echo "Error: installing Flask failed."
    echo "Please ensure it's added to your path."
    exit 1 
fi

echo "Checking if Virtual Env Running"
if command echo $VIRTUAL_ENV | grep basketball-stats/venv &> /dev/null; then
    echo "Virtual environment already running."
else 
    echo "Virtual environmeny not setup. Attempting to create..."
    python3 -m venv venv
    source venv/bin/activate
fi 

if ! command echo $VIRTUAL_ENV | grep basketball-stats/venv &> /dev/null
then
    echo "Error: starting virtual env."
    exit 1 
fi
