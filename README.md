# GazaGrid: Quantum-Inspired Energy Optimization for Gaza

**The first system in Palestine using quantum-inspired algorithms to optimize renewable energy site selection in Gaza.**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-0.45+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
## Problem Statement

In Gaza today, electricity is available for only **4–6 hours per day**, creating severe challenges for healthcare, education, industry, and daily life.

**GazaGrid** addresses this critical issue by providing an intelligent, data-driven solution to identify **optimal locations for solar and wind energy installations** using **advanced quantum-inspired optimization algorithms**, maximizing energy efficiency under real-world constraints.
## Key Features

- **Smart Geographic Analysis**  
  Interactive map of Gaza using realistic, location-based data.

- **Advanced Optimization Algorithms**  
  Quantum-inspired optimization using **QAOA** for optimal renewable energy site selection.

- **Multi-Criteria Decision Analysis (MCDA)**  
  Integrated evaluation of **solar potential, wind resources, risk levels, and distance to the power grid**.

- **Complete Interactive Dashboard**  
  Streamlit-based dashboard with advanced data visualizations and insights.

- **Data Export Capabilities**  
  Export optimized site selections in **CSV** and **JSON** formats for further analysis.
## Technology Stack

- **Python 3.11+**  
  Main programming language powering the entire system.

- **Streamlit**  
  Interactive web application framework for building the dashboard.

- **Qiskit**  
  Quantum computing framework used for quantum-inspired optimization algorithms.

- **Pandas & NumPy**  
  Data processing, numerical computation, and analysis.

- **Folium**  
  Interactive mapping and geographic data visualization.

- **Scikit-learn**  
  Machine learning utilities for preprocessing and analytical support.

## Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/gazagrid.git
cd gazagrid

# 2. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data
python data_generator.py

# 5. Run the application
streamlit run app.py
```
## How It Works

### Step 1: Data Analysis

The system analyzes **45 locations** across the Gaza Strip based on the following attributes:

- Geographic coordinates (latitude and longitude)
- Solar irradiance (4.5–6.0 kWh/m²/day)
- Wind speed (2.5–6.5 m/s)
- Risk score (scale from 0 to 10)
- Distance from the existing power grid (in meters)
- Accessibility status
### Step 2: Suitability Scoring

Each candidate location is evaluated using a weighted suitability function that balances energy potential against practical constraints:
Suitability_Score = (solar × solar_weight) + (wind × wind_weight) - (risk × risk_weight) - (grid_distance × grid_weight)
### Step 3: Quantum-Inspired Optimization

The optimal set of renewable energy sites is selected using a **Quantum Approximate Optimization Algorithm (QAOA)** simulated via Qiskit.  
Rather than selecting sites independently, the optimizer evaluates combinations of locations to maximize overall system efficiency under constraints.

```python
# Using Quantum Approximate Optimization Algorithm (QAOA)
optimizer = QuantumEnergyOptimizer(n_sites_to_select=5)
selected_indices = optimizer.optimize(
    suitability_scores,
    coordinates,
    risk_scores
)
```
### Step 4: Results Visualization

The final selected sites and their performance metrics are presented through an interactive dashboard, which includes:

- An interactive map highlighting the selected locations
- Detailed performance metrics for each site
- Comparative analysis and spatial distribution of the chosen locations


## Dashboard Features

- **Sidebar Configuration**  
  Adjust suitability weights, select the number of sites, and control algorithm parameters.

- **Interactive Map**  
  Visual representation of all candidate locations with selected sites highlighted.

- **Performance Metrics**  
  Real-time calculations of energy potential for each selected location.

- **Data Tables**  
  Detailed tabular information about the selected sites.

- **Export Options**  
  Download optimized site selections in **CSV** or **JSON** format for further analysis.

