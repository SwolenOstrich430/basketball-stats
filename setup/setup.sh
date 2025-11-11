#! bin/bash

echo "Checking if pip Installed" 
if command pip3 --version | grep -E 'pip [0-9]{1,3}'; then
    echo "pip is installed."
else
    echo "pip is not installed. Attempting to install it..."
    python3 -m ensurepip --upgrade 
    pip_path=$(which pip3)
    echo "export PATH=/usr/bin/pip3:\$PATH"  | cat - ~/.zshrc > /tmp/zshrc_temp && mv /tmp/zshrc_temp ~/.zshrc
    python3 -m pip install --upgrade pip
fi


if ! command pip3 --version | grep -E 'pip [0-9]{1,3}'; then
    echo "Error: pip is not installed or not found in your PATH."
    echo "Please install pip or ensure it's added to your system's PATH."
    exit 1 
fi

echo "Checking if Flask Installed"
if command pip3 list | grep Flask &> /dev/null; then
    echo "Flask already installed."
else 
    echo "Flask not installed. Attempting to install it..."
    pip3 install Flask
fi 

if ! command pip3 list | grep Flask &> /dev/null
then
    echo "Error: installing Flask failed."
    echo "Please ensure it's added to your path."
    exit 1 
fi