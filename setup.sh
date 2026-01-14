#!/bin/bash

# EMO AI Backend - Quick Start Script
# This script helps you get started quickly!

echo "🤖 EMO AI Backend - Quick Start"
echo "================================"
echo ""

# Check if PostgreSQL is running
echo "📊 Checking PostgreSQL..."
if systemctl is-active --quiet postgresql; then
    echo "✅ PostgreSQL is running!"
else
    echo "❌ PostgreSQL is not running!"
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
fi

echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with UV..."
    uv venv
    echo "✅ Virtual environment created!"
else
    echo "✅ Virtual environment already exists!"
fi

echo ""

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source .venv/bin/activate
uv pip install -e .

echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from example..."
    cp .env.example .env
    echo "✅ Created .env file!"
    echo "⚠️  IMPORTANT: Edit .env and add your OpenCode.Zen API key!"
    echo ""
else
    echo "✅ .env file already exists!"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenCode.Zen API key"
echo "2. Run: source .venv/bin/activate"
echo "3. Run: uvicorn app.main:app --reload"
echo ""
echo "Or simply run: ./run.sh"
echo ""
echo "*bounces excitedly* EMO is ready to chat! 💕"
