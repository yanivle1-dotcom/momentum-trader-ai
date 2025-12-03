#!/bin/bash

# Setup script for Momentum Trader AI

echo "╔═══════════════════════════════════════════════╗"
echo "║   Momentum Trader AI - Ross Cameron System   ║"
echo "║              Setup Script                     ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

# Create .env file if not exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file and add your API keys!"
    echo "   nano .env"
    echo ""
else
    echo ""
    echo "✅ .env file already exists"
fi

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║            Setup Complete! 🎉                 ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys:"
echo "   nano .env"
echo ""
echo "2. Run the application:"
echo "   cd src/web && python app.py"
echo ""
echo "3. Open browser:"
echo "   http://localhost:5000"
echo ""
echo "For help, see README.md or QUICKSTART.md"
echo ""
