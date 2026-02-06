import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import json
import os
import sys
# تأكد من وجود ملف quantum_logic.py في نفس المجلد
try:
    from quantum_logic import QuantumEnergyOptimizer
except ImportError:
    st.error("System Error: quantum_logic module not found.")
    st.stop()
import time

# --- Page Configuration (Professional Setup) ---
st.set_page_config(
    page_title="GazaGrid Infrastructure Planning",
    page_icon=None, # Removed Emoji
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Engineering Theme (CSS) ---
st.markdown("""
<style>
    /* Global Font & Colors */
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1f2937;
        background-color: #f9fafb;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827; /* Dark Navy */
        margin-bottom: 0.2rem;
        letter-spacing: -0.025em;
    }
    .subtitle {
        color: #6b7280; /* Cool Gray */
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 1rem;
    }

    /* Cards (Metrics & Info) */
    .metric-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: box-shadow 0.3s ease;
    }
    .metric-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
        margin-top: 0.5rem;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0f172a; /* Corporate Blue/Black */
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #1e293b;
        transform: translateY(-1px);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f3f4f6;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Custom Info Box */
    .methodology-box {
        background-color: #ffffff;
        border-left: 4px solid #0f172a;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 2rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'optimized' not in st.session_state:
    st.session_state.optimized = False
if 'selected_sites' not in st.session_state:
    st.session_state.selected_sites = []

# --- Data Handling ---
@st.cache_data
def load_data():
    """Load or Generate the Gaza energy data."""
    data_path = "gaza_energy_data.csv"
    if not os.path.exists(data_path):
        from data_generator import GazaDataGenerator # Assuming class name
        # Fallback if generator logic is different, adapt as needed
        # simple generation for demo
        try:
            gen = GazaDataGenerator()
            df = gen.generate_realistic_data(45)
        except:
             # Basic fallback if module differs
            st.error("Data Generator module error. Please ensure data_generator.py exists.")
            st.stop()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
    return df

def calculate_suitability_score(df, solar_w, wind_w, risk_w, grid_w):
    """MCDA Calculation Logic."""
    # Filter accessible sites
    df_filtered = df[df['Accessibility'] == 1].copy()
    
    # Normalization (Min-Max)
    cols = {'Solar_Irradiance': solar_w, 'Wind_Speed': wind_w, 
            'Risk_Score': -risk_w, 'Grid_Distance': -grid_w} # negative for penalties
    
    df_filtered['Suitability_Score'] = 0
    
    for col, weight in cols.items():
        min_val = df_filtered[col].min()
        max_val = df_filtered[col].max()
        norm = (df_filtered[col] - min_val) / (max_val - min_val)
        if weight < 0: # Penalty
            df_filtered['Suitability_Score'] -= norm * abs(weight)
        else: # Benefit
            df_filtered['Suitability_Score'] += norm * weight
            
    # Scale to 0-100 for readability
    s_min = df_filtered['Suitability_Score'].min()
    s_max = df_filtered['Suitability_Score'].max()
    df_filtered['Suitability_Score'] = ((df_filtered['Suitability_Score'] - s_min) / (s_max - s_min)) * 100
    
    return df_filtered

def create_professional_map(df, selected_indices=None):
    """Folium map with professional markers."""
    center_lat, center_lon = 31.4167, 34.3333
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='CartoDB positron' # Cleaner, more professional map style
    )
    
    for idx, row in df.iterrows():
        # Logic for styling
        is_selected = selected_indices is not None and idx in selected_indices
        
        if is_selected:
            color = '#10B981' # Emerald Green
            radius = 8
            fill_opacity = 0.9
            tooltip_txt = "Selected Site"
        elif row['Accessibility'] == 0:
            color = '#9CA3AF' # Gray
            radius = 3
            fill_opacity = 0.5
            tooltip_txt = "Restricted Zone"
        elif row['Risk_Score'] > 7:
            color = '#EF4444' # Red
            radius = 4
            fill_opacity = 0.6
            tooltip_txt = "High Risk Zone"
        else:
            color = '#3B82F6' # Blue
            radius = 5
            fill_opacity = 0.6
            tooltip_txt = "Candidate Site"

        # Content for popup
        popup_content = f"""
        <div style="font-family: sans-serif; min-width: 150px;">
            <strong style="color: {color}">{tooltip_txt}</strong><br>
            <div style="margin-top: 5px; font-size: 12px; color: #374151;">
                ID: {row['Region_ID']}<br>
                Solar: {row['Solar_Irradiance']:.2f} kWh<br>
                Risk Index: {row['Risk_Score']}/10
            </div>
        </div>
        """

        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=fill_opacity,
            popup=folium.Popup(popup_content, max_width=200),
            tooltip=tooltip_txt
        ).add_to(m)
    
    return m

def export_data(df, indices, file_format):
    selected = df.loc[indices].copy()
    if file_format == 'CSV':
        return selected.to_csv(index=False)
    return selected.to_json(orient='records', indent=2)

# --- Main Interface ---

# Header Section
st.markdown('<div class="main-header">GazaGrid Infrastructure Planning</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Advanced Site Selection System for Renewable Energy Deployment</div>', unsafe_allow_html=True)

df = load_data()

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### System Configuration")
    
    st.markdown("#### Optimization Constraints")
    n_sites = st.number_input("Target Number of Sites", min_value=1, max_value=20, value=5)
    circuit_depth = st.select_slider("Computation Depth (QAOA Layers)", options=[1, 2, 3], value=2)
    
    st.markdown("#### Decision Weighting (MCDA)")
    w_solar = st.slider("Solar Potential Importance", 0.0, 1.0, 0.5)
    w_wind = st.slider("Wind Potential Importance", 0.0, 1.0, 0.3)
    w_risk = st.slider("Risk Avoidance Factor", 0.0, 1.0, 0.4)
    w_grid = st.slider("Grid Proximity Importance", 0.0, 0.01, 0.001, format="%.4f")
    
    st.markdown("---")
    
    run_btn = st.button("Initialize Optimization Analysis")

# --- Logic Execution ---
if run_btn:
    with st.spinner("Processing geospatial data and executing quantum algorithms..."):
        # 1. Classical Processing
        df_scored = calculate_suitability_score(df, w_solar, w_wind, w_risk, w_grid)
        
        # 2. Quantum Processing
        # Preparing numpy arrays for the optimizer
        scores_array = df_scored['Suitability_Score'].values
        coords_array = df_scored[['Latitude', 'Longitude']].values
        risks_array = df_scored['Risk_Score'].values
        
        # Instantiate Optimizer
        optimizer = QuantumEnergyOptimizer(n_sites_to_select=n_sites, qaoa_layers=circuit_depth)
        
        # Execute Solve
        # Note: Removing progress_callback for cleaner UI unless strictly needed
        selected_rel_indices, energy_val = optimizer.optimize(
            scores_array, coords_array, risks_array
        )
        
        # Map results
        selected_indices = df_scored.index[selected_rel_indices].tolist()
        
        # Save State
        st.session_state.optimized = True
        st.session_state.selected_sites = selected_indices
        st.session_state.df_scored = df_scored
        st.session_state.energy_val = energy_val
        
        time.sleep(0.5) # UI smoothing
        st.rerun()

# --- Dashboard Content ---

if not st.session_state.optimized:
    # Methodology View
    st.markdown("""
    <div class="methodology-box">
        <h3 style="margin-top:0;">System Methodology</h3>
        <p>This platform utilizes a hybrid quantum-classical approach to solve the facility location problem under conflict constraints.</p>
        <ol>
            <li><strong>Data Ingestion:</strong> Parsing geospatial coordinates, solar irradiance maps, and risk indices.</li>
            <li><strong>Multi-Criteria Analysis:</strong> Normalizing conflicting objectives (Safety vs. Efficiency).</li>
            <li><strong>Quantum Approximation:</strong> Utilizing QAOA to explore the solution space for optimal site configuration.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="metric-card"><div class="metric-label">Total Candidate Sites</div><div class="metric-value">{len(df)}</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-label">Viable Locations</div><div class="metric-value">{len(df[df['Accessibility']==1])}</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="metric-card"><div class="metric-label">Avg. Solar Potential</div><div class="metric-value">{df['Solar_Irradiance'].mean():.2f} <span style="font-size:1rem">kWh</span></div></div>""", unsafe_allow_html=True)
    
    st.markdown("### Geospatial Visualization")
    st_map = create_professional_map(df)
    folium_static(st_map, width=1400, height=500)

else:
    # Results View
    df_res = st.session_state.df_scored
    sel_sites = st.session_state.selected_sites
    sel_df = df_res.loc[sel_sites]
    
    st.markdown("### Optimization Results")
    
    # Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    total_cap = sel_df['Solar_Irradiance'].sum() * 100 # Assumption factor
    avg_suit = sel_df['Suitability_Score'].mean()
    
    c1.markdown(f"""<div class="metric-card"><div class="metric-label">Selected Sites</div><div class="metric-value">{len(sel_sites)}</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-label">Est. Generation Capacity</div><div class="metric-value">{total_cap:.0f} <span style="font-size:1rem">kW</span></div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="metric-card"><div class="metric-label">Risk Index (Avg)</div><div class="metric-value">{sel_df['Risk_Score'].mean():.1f}<span style="font-size:1rem">/10</span></div></div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="metric-card"><div class="metric-label">Optimization Score</div><div class="metric-value">{avg_suit:.1f}<span style="font-size:1rem">%</span></div></div>""", unsafe_allow_html=True)
    
    # Map
    st.markdown("### Strategic Deployment Map")
    res_map = create_professional_map(df_res, sel_sites)
    folium_static(res_map, width=1400, height=500)
    
    # Table & Export
    st.markdown("### Location Data Specification")
    
    # Clean table for report
    clean_table = sel_df[['Region_ID', 'Latitude', 'Longitude', 'Solar_Irradiance', 'Risk_Score', 'Suitability_Score']].copy()
    clean_table.columns = ['Region ID', 'Lat', 'Lon', 'Solar (kWh)', 'Risk Factor', 'Score']
    st.dataframe(clean_table, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        csv = export_data(df_res, sel_sites, 'CSV')
        st.download_button("Download Report (CSV)", csv, "optimization_report.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 0.8rem; color: #9ca3af;">
    GazaGrid Infrastructure Planning System v1.0 | Research Prototype
</div>
""", unsafe_allow_html=True)
