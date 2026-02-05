#!/bin/bash

# GazaGrid Startup Script

echo "🚀 Starting GazaGrid: Quantum Energy Optimizer"
echo "============================================="

# Navigate to project directory
cd /app/gazagrid

# Check if data file exists, generate if not
if [ ! -f "gaza_energy_data.csv" ]; then
    echo "📊 Generating synthetic Gaza energy data..."
    python data_generator.py
    echo "✅ Data generation complete!"
else
    echo "✅ Data file already exists"
fi

echo ""
echo "🌐 Starting Streamlit application..."
echo "📍 Access the dashboard at: http://localhost:8501"
echo ""

# Run Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
