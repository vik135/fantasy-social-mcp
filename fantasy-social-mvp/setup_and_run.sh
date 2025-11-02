#!/bin/bash
# One-click setup script for Mac/Linux

echo "🏈 Fantasy Football Social - Easy Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed!"
    echo "📥 Please install Python from: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Ask if user wants test data
read -p "Would you like to create test data? (y/n): " create_test
if [ "$create_test" = "y" ] || [ "$create_test" = "Y" ]; then
    echo "📊 Creating test data..."
    python3 create_test_data.py
    echo "✓ Test data created!"
    echo ""
    echo "Test usernames: fantasy_guru, the_commish, waiver_wire_king, taco_tuesday, analytics_andy"
fi

echo ""
echo "🚀 Starting the app..."
echo "📱 The app will open in your browser automatically"
echo "🔗 If not, go to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the app"
echo ""

# Run the app
streamlit run app.py
