#!/bin/bash

# Setup script for installing Rill and its dependencies

echo "Setting up Rill for DSP Reports Dashboard"

# Ensure we're in a Python virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Creating and activating a virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
else
    echo "Using existing virtual environment: ${VIRTUAL_ENV}"
fi

# Install required Python packages
echo "Installing required Python packages..."
pip install pymongo python-dotenv pandas pyyaml

# Install Rill CLI
echo "Installing Rill CLI..."
pip install rilldata

# Link the MongoDB .env file
if [[ ! -f rill-dashboards/.env ]]; then
    echo "Linking MongoDB environment variables..."
    ln -s ../.env rill-dashboards/.env
fi

echo "Installation complete!"
echo "To start Rill, run: cd rill-dashboards && rill start" 