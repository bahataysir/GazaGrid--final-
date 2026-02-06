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
  Export optimized site selections in **CSV** and **JSON** formats for further analysis

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

## Sample Results

| Site ID         | Solar Potential       | Risk Score | Suitability |
|-----------------|---------------------|------------|------------|
| North_Gaza_04   | 5.8 kWh/m²/day      | 3/10       | 0.92       |
| Gaza_City_12    | 5.3 kWh/m²/day      | 5/10       | 0.85       |
| Khan_Younis_22  | 5.6 kWh/m²/day      | 2/10       | 0.94       |

**Example Output:** Selecting 5 optimal sites can:

- Generate approximately **125 kWh per day**
- Power up to **50 households**
- Maintain an average risk score below **4.2/10**

## Methodology

### Classical AI Component (MCDA)

The **Multi-Criteria Decision Analysis (MCDA)** evaluates each candidate site using multiple factors to determine its suitability for renewable energy installation:

1. **Solar energy potential**  
2. **Wind energy potential**  
3. **Security risk assessment**  
4. **Distance to existing power grid**  
5. **Geographic accessibility**

### Quantum-Inspired Component (QAOA)

The **Quantum Approximate Optimization Algorithm (QAOA)** addresses the combinatorial optimization problem of selecting the best set of renewable energy sites:

- **Objective:** Maximize the total suitability score across selected sites  
- **Constraint:** Select exactly **N** sites  
- **Penalty:** Discourage geographic clustering of selected sites  
- **Reward:** Favor sites with low risk and high energy potential

## Future Enhancements

Planned improvements for GazaGrid include:

- **Integration with real UNRWA data** for more accurate site analysis  
- **Cost-benefit analysis module** to evaluate economic feasibility  
- **Web API** for programmatic access to site selection results  
- **Real-time weather data integration** to account for daily variability  
- **Mobile application interface** for on-the-go access  
- **Arabic language support** to improve accessibility for local users

## Development Team

- Sarah Abumandil  
- Bahaa Amro

Contributing

1. Fork the repository


2. Create a feature branch (git checkout -b feature/NewFeature)


3. Commit your changes (git commit -m 'Add NewFeature')


4. Push to the branch (git push origin feature/NewFeature)


5. Open a Pull Request



# GazaGrid

**Clean Energy for Gaza, Advanced Technology for Palestine**
