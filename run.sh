#!/bin/bash

# Run script for Momentum Trader AI

echo "🚀 Starting Momentum Trader AI..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please run setup.sh first:"
    echo "   bash setup.sh"
    exit 1
fi

# Run the application
cd src/web
python app.py
