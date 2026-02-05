# 🌍 GazaGrid: Resilient Quantum Energy Optimizer

## Overview

GazaGrid is a hackathon-winning prototype that combines Classical AI with Quantum Computing to optimize renewable energy placement in the Gaza Strip. The system uses Multi-Criteria Decision Analysis (MCDA) for preprocessing and Quantum Approximate Optimization Algorithm (QAOA) for finding optimal site combinations.

## 🎯 Features

- **Hybrid AI-Quantum Processing**: Classical MCDA + Qiskit QAOA
- **Interactive Dashboard**: Built with Streamlit
- **Real-time Optimization**: Adjustable parameters with live updates
- **Geographic Visualization**: Folium maps with color-coded markers
- **Export Functionality**: Download results as CSV or JSON
- **Risk-Aware Selection**: Penalizes high-risk conflict zones
- **Decentralization**: Encourages geographic spread for grid resilience

## 📁 Project Structure

```
/app/gazagrid/
├── app.py                    # Main Streamlit dashboard
├── quantum_logic.py          # QAOA optimization engine
├── data_generator.py         # Synthetic data generator
├── gaza_energy_data.csv      # Generated dataset (40-50 points)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Installation

1. Install dependencies:
```bash
cd /app/gazagrid
pip install -r requirements.txt
```

2. Generate data (if not exists):
```bash
python data_generator.py
```

3. Run the application:
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🎮 Usage

1. **Configure Parameters** (Sidebar):
   - Number of sites to select (3-15)
   - QAOA circuit depth (1-3 layers)
   - Adjust MCDA weights:
     - Solar irradiance importance
     - Wind speed importance
     - Risk penalty factor
     - Grid distance penalty

2. **Run Optimization**:
   - Click "🚀 Run Quantum Optimization"
   - Wait 30-60 seconds for QAOA to complete
   - View results on interactive map

3. **Export Results**:
   - Download optimal sites as CSV or JSON
   - Share with stakeholders or use in other systems

## 🧮 Algorithm Details

### Classical AI (MCDA)

Suitability Score Formula:
```
Score = (Solar × 0.5) + (Wind × 0.3) - (Risk × 0.4) - (GridDist × 0.001)
```

- Filters out inaccessible locations (Accessibility == 0)
- Normalizes all features to 0-1 range
- Produces suitability score for each site

### Quantum Optimization (QAOA)

**Problem**: Select N sites that maximize total suitability

**Formulation**: QUBO (Quadratic Unconstrained Binary Optimization)

**Objective Function**:
- Maximize: Sum of suitability scores
- Penalize: High-risk areas (Risk_Score > 7)
- Encourage: Geographic spread (distance-based penalty)

**Constraints**:
- Exactly N sites must be selected (equality constraint)
- All selected sites must be accessible

**Implementation**:
- Qiskit QAOA with Aer simulator
- COBYLA optimizer for variational parameters
- 2-layer quantum circuit (configurable)
- Fallback to greedy selection if QAOA fails

## 📊 Dataset

### Columns:
- **Region_ID**: Unique identifier (e.g., "North_Gaza_01")
- **Latitude/Longitude**: GPS coordinates within Gaza boundaries
- **Solar_Irradiance**: kWh/m²/day (4.5-6.0 range)
- **Wind_Speed**: m/s (2.5-6.5 range, higher near coast)
- **Risk_Score**: 0-10 (0=safe, 10=high conflict zone)
- **Accessibility**: Binary (1=accessible, 0=restricted buffer zone)
- **Grid_Distance**: Meters to nearest existing grid node

### Data Generation Logic:
- 40-50 synthetic points across Gaza Strip
- Coastal areas: Higher wind speeds
- Border regions: Higher risk scores
- ~20% locations marked as inaccessible
- Realistic coordinate ranges (31.25°N-31.58°N, 34.20°E-34.55°E)

## 🎨 Map Legend

- 🟢 **Green (Bolt)**: Selected optimal sites
- 🔵 **Blue (Info)**: Candidate sites (accessible, low-med risk)
- 🔴 **Red (Warning)**: High-risk zones (Risk > 7)
- ⚫ **Gray (Ban)**: Inaccessible/restricted areas

## 🏆 Innovation Highlights

1. **Quantum Advantage**: Uses QAOA to solve NP-hard combinatorial optimization
2. **Context-Aware**: Explicitly models geopolitical risk and grid resilience
3. **Decentralization**: Encourages distributed energy generation
4. **Real-time Adaptability**: Stakeholders can adjust priorities dynamically
5. **Practical Implementation**: Runs on classical simulator, ready for real quantum hardware

## 🔧 Technical Notes

- **QAOA Execution Time**: 30-60 seconds for 40-50 sites
- **Circuit Depth**: Higher layers = better accuracy but slower
- **Fallback Strategy**: Greedy selection if QAOA constraint violation
- **Quantum Backend**: Qiskit Aer simulator (can be swapped for real quantum devices)

## 📈 Future Enhancements

- Real-world data integration (NASA POWER API, conflict databases)
- Multi-objective optimization (cost, maintenance, etc.)
- Temporal analysis (seasonal variations)
- Integration with existing grid infrastructure data
- Real quantum hardware deployment (IBMQ)

## 🌟 Impact

This system demonstrates how quantum computing can solve real-world infrastructure challenges in conflict zones, balancing:
- **Energy Production**: Maximizing renewable output
- **Safety**: Avoiding high-risk areas
- **Resilience**: Ensuring grid stability through decentralization
- **Accessibility**: Respecting physical constraints

---

**Built with**: Qiskit • Streamlit • Folium • Python

**For**: Hackathon demonstration and proof-of-concept
