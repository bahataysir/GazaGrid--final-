# 🚀 GazaGrid Quick Start Guide

## Access the Application

**Dashboard URL:** `http://localhost:8501`

The application is currently running and accessible via the above URL.

---

## 🎯 How to Use

### Step 1: Configure Parameters (Left Sidebar)

#### Optimization Parameters:
- **Number of Sites to Select**: Use slider to choose 3-15 optimal locations (default: 5)
- **QAOA Circuit Depth**: Select 1-3 layers (higher = better accuracy but slower)
  - 1 layer: ~15-30 seconds
  - 2 layers: ~30-60 seconds  
  - 3 layers: ~60-90 seconds

#### MCDA Weights:
Adjust importance of each factor (0.0 to 1.0):
- ☀️ **Solar Irradiance** (default: 0.50) - Priority for solar energy potential
- 💨 **Wind Speed** (default: 0.30) - Priority for wind energy potential
- ⚠️ **Risk Penalty** (default: 0.40) - Avoid high-risk conflict zones
- 📍 **Grid Distance Penalty** (default: 0.001) - Prefer sites closer to existing grid

### Step 2: Run Optimization

Click the **"🚀 Run Quantum Optimization"** button

The system will:
1. Apply MCDA scoring to filter and rank sites
2. Run QAOA quantum algorithm to find optimal combinations
3. Display results on interactive map

⏱️ **Expected time**: 30-60 seconds depending on circuit depth

### Step 3: Review Results

After optimization completes, you'll see:

#### Performance Metrics:
- Total Solar Potential (kWh/m²/day)
- Total Wind Potential (m/s)
- Average Risk Score (0-10)
- Average Suitability Score (0-1)

#### Interactive Map:
- 🟢 **Green markers** = Selected optimal sites
- 🔵 **Blue markers** = Candidate sites (accessible, low-med risk)
- 🔴 **Red markers** = High-risk zones (Risk > 7)
- ⚫ **Gray markers** = Inaccessible/restricted areas

Click any marker to see detailed information!

#### Selected Sites Table:
Full details of chosen locations including coordinates, energy potential, and risk scores

#### Distribution Analysis:
- Regional spread of selected sites
- Risk level breakdown

### Step 4: Export Results

Use the export buttons in the sidebar:
- **CSV** - Spreadsheet format with all site details
- **JSON** - Structured data for integration with other systems

---

## 🔧 Understanding the Algorithm

### Classical AI (MCDA)
Evaluates each location using weighted formula:
```
Score = (Solar × 0.5) + (Wind × 0.3) - (Risk × 0.4) - (GridDist × 0.001)
```

### Quantum Optimization (QAOA)
Solves combinatorial problem:
- **Objective**: Maximize total energy potential
- **Constraints**: Select exactly N sites, all must be accessible
- **Penalties**: Heavy penalty for high-risk areas (Risk > 7)
- **Decentralization**: Encourages geographic spread for grid resilience

---

## 📊 Dataset Information

**Total Locations**: 45 points across Gaza Strip
- **Accessible Sites**: 32 (71%)
- **High Risk Zones**: 4 (9%)
- **Regions**: North Gaza, Gaza City, Deir al-Balah, Khan Younis, Rafah

### Data Columns:
- Region_ID, Latitude, Longitude
- Solar_Irradiance (4.5-6.0 kWh/m²/day)
- Wind_Speed (2.5-6.5 m/s, higher near coast)
- Risk_Score (0-10, 0=safe, 10=conflict zone)
- Accessibility (1=accessible, 0=restricted)
- Grid_Distance (meters to nearest grid node)

---

## 🎓 Tips for Best Results

1. **Prioritize Safety**: Increase Risk Penalty weight (0.6-0.8) to strongly avoid high-risk areas
2. **Maximize Energy**: Increase Solar and Wind weights when energy production is priority
3. **Balance Approach**: Use default weights for balanced optimization
4. **Quick Testing**: Use 1 QAOA layer and 3 sites for fast results
5. **Production Run**: Use 2-3 layers and 5-10 sites for best quality

---

## 🐛 Troubleshooting

**Page won't load?**
- Ensure Streamlit is running on port 8501
- Check: `ps aux | grep streamlit`
- Restart: `cd /app/gazagrid && ./run.sh`

**Optimization taking too long?**
- Reduce QAOA layers to 1
- Reduce number of sites to 3-5
- This is normal for quantum algorithms!

**No green markers after optimization?**
- Check if optimization completed successfully
- Look for success message at top of page
- Try adjusting parameters and run again

---

## 🌟 Advanced Usage

### Modifying the Dataset
Edit `gaza_energy_data.csv` or regenerate:
```bash
cd /app/gazagrid
python data_generator.py
```

### Running from Command Line
```bash
cd /app/gazagrid
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Testing Quantum Engine
```bash
cd /app/gazagrid
python test_system.py
```

---

## 📚 Technical Details

- **Framework**: Streamlit (Dashboard) + Qiskit (Quantum)
- **Quantum Backend**: Aer Simulator (can be replaced with real quantum hardware)
- **Algorithm**: QAOA (Quantum Approximate Optimization Algorithm)
- **Optimizer**: COBYLA (Constrained Optimization BY Linear Approximations)
- **Map Library**: Folium (Interactive Leaflet.js maps)

---

## 🤝 Support

For technical details, see:
- `README.md` - Full project documentation
- `quantum_logic.py` - QAOA implementation details
- `app.py` - Streamlit dashboard code

---

**Built for:** Hackathon demonstration of quantum computing for real-world infrastructure challenges

**Impact:** Balances renewable energy production, safety, and grid resilience in conflict zones
