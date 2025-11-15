#!/bin/bash
# =================================================================
# CRA Chatbot - Development Environment Setup Script
# =================================================================

set -e  # Exit on error

echo "🚀 Setting up CRA Chatbot development environment..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10.0"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"; then
    echo "❌ Error: Python 3.10+ required (found $python_version)"
    exit 1
fi
echo "✅ Python $python_version detected"
echo ""

# Create virtual environment
echo "🔨 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    else
        echo "ℹ️  Using existing virtual environment"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "   This may take 5-10 minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
echo "🔑 Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    cp .env.template .env
    echo "✅ .env file created from template"
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
fi
echo ""

# Create necessary directories
echo "📁 Ensuring data directories exist..."
mkdir -p data/raw data/processed data/ground_truth logs
mkdir -p models checkpoints
echo "✅ Directories created"
echo ""

# Download NLTK data (if needed)
echo "📚 Downloading required NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo "✅ NLTK data downloaded"
echo ""

# Test configuration loading
echo "🧪 Testing configuration..."
python3 config/settings.py
if [ $? -eq 0 ]; then
    echo "✅ Configuration test passed"
else
    echo "⚠️  Configuration test failed - make sure to set API keys in .env"
fi
echo ""

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API keys:"
echo "     - ANTHROPIC_API_KEY (Claude 3.5 Sonnet)"
echo "     - OPENAI_API_KEY (Embeddings)"
echo "     - COHERE_API_KEY (Reranking)"
echo "     - QDRANT_URL and QDRANT_API_KEY (Vector DB)"
echo ""
echo "  2. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Start collecting CRA documentation:"
echo "     python -m src.data_collection.scraper"
echo ""
echo "  4. Run tests:"
echo "     pytest"
echo ""
echo "Happy coding! 🎉"
