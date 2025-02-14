#!/bin/bash

# Set the name for your virtual environment
VENV_NAME="venv"

# Check if the virtual environment already exists
if [ ! -d "$VENV_NAME" ]; then
  echo "Creating virtual environment..."
  python3 -m venv $VENV_NAME
else
  echo "Virtual environment already exists."
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install requests spotipy pandas

echo "Setup complete. Virtual environment is ready!"
exec bash
