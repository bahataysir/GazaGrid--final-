import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import json
import os
import sys
from quantum_logic import QuantumEnergyOptimizer
import time

# Page config
st.set_page_config(
    page_title="GazaGrid: Quantum Energy Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102,126,234,0.4);
    }
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'optimized' not in st.session_state:
    st.session_state.optimized = False
if 'selected_sites' not in st.session_state:
    st.session_state.selected_sites = []

@st.cache_data
def load_data():
    """Load the Gaza energy data."""
    data_path = "gaza_energy_data.csv"
    if not os.path.exists(data_path):
        # Generate data if not exists
        from data_generator import generate_gaza_energy_data
        df = generate_gaza_energy_data(45)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
    return df

def calculate_suitability_score(df, solar_weight, wind_weight, risk_weight, grid_weight):
    """
    Calculate suitability score using MCDA.
    """
    # Filter accessible sites only
    df_filtered = df[df['Accessibility'] == 1].copy()
    
    # Normalize features to 0-1 range
    solar_norm = (df_filtered['Solar_Irradiance'] - df_filtered['Solar_Irradiance'].min()) / \
                 (df_filtered['Solar_Irradiance'].max() - df_filtered['Solar_Irradiance'].min())
    
    wind_norm = (df_filtered['Wind_Speed'] - df_filtered['Wind_Speed'].min()) / \
                (df_filtered['Wind_Speed'].max() - df_filtered['Wind_Speed'].min())
    
    risk_norm = (df_filtered['Risk_Score'] - df_filtered['Risk_Score'].min()) / \
                (df_filtered['Risk_Score'].max() - df_filtered['Risk_Score'].min())
    
    grid_norm = (df_filtered['Grid_Distance'] - df_filtered['Grid_Distance'].min()) / \
                (df_filtered['Grid_Distance'].max() - df_filtered['Grid_Distance'].min())
    
    # Calculate weighted score
    df_filtered['Suitability_Score'] = (
        solar_norm * solar_weight +
        wind_norm * wind_weight -
        risk_norm * risk_weight -
        grid_norm * grid_weight
    )
    
    # Normalize to 0-1
    min_score = df_filtered['Suitability_Score'].min()
    max_score = df_filtered['Suitability_Score'].max()
    df_filtered['Suitability_Score'] = (df_filtered['Suitability_Score'] - min_score) / (max_score - min_score)
    
    return df_filtered

def create_map(df, selected_indices=None):
    """
    Create Folium map with markers.
    """
    # Center of Gaza Strip
    center_lat = 31.4167
    center_lon = 34.3333
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add markers
    for idx, row in df.iterrows():
        # Determine marker color
        if selected_indices is not None and idx in selected_indices:
            color = 'green'
            icon = 'bolt'
            popup_prefix = "⚡ SELECTED"
        elif row['Accessibility'] == 0:
            color = 'gray'
            icon = 'ban'
            popup_prefix = "🚫 RESTRICTED"
        elif row['Risk_Score'] > 7:
            color = 'red'
            icon = 'exclamation-triangle'
            popup_prefix = "⚠️ HIGH RISK"
        else:
            color = 'blue'
            icon = 'info-sign'
            popup_prefix = "📍 CANDIDATE"
        
        # Create popup text
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px; width: 200px;">
            <h4 style="margin: 0; color: {color};">{popup_prefix}</h4>
            <hr style="margin: 5px 0;">
            <b>Region:</b> {row['Region_ID']}<br>
            <b>Location:</b> ({row['Latitude']:.4f}, {row['Longitude']:.4f})<br>
            <b>Solar:</b> {row['Solar_Irradiance']:.2f} kWh/m²/day<br>
            <b>Wind:</b> {row['Wind_Speed']:.2f} m/s<br>
            <b>Risk Score:</b> {row['Risk_Score']}/10<br>
            <b>Grid Distance:</b> {row['Grid_Distance']}m<br>
        """
        
        if 'Suitability_Score' in row:
            popup_html += f"<b>Suitability:</b> {row['Suitability_Score']:.3f}<br>"
        
        popup_html += "</div>"
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color, icon=icon),
            tooltip=row['Region_ID']
        ).add_to(m)
    
    return m

def export_results(df, selected_indices, format='csv'):
    """
    Export selected sites data.
    """
    selected_df = df.loc[selected_indices].copy()
    
    if format == 'csv':
        return selected_df.to_csv(index=False)
    elif format == 'json':
        return selected_df.to_json(orient='records', indent=2)

# Main App
st.markdown('<h1 class="main-header">⚡ GazaGrid: Resilient Quantum Energy Optimizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Hybrid AI-Quantum System for Optimal Renewable Energy Placement</p>', unsafe_allow_html=True)

# Load data
df = load_data()

# Sidebar
with st.sidebar:
    st.header("🎛️ Configuration")
    
    st.subheader("Optimization Parameters")
    n_sites = st.slider(
        "Number of Sites to Select",
        min_value=3,
        max_value=15,
        value=5,
        help="Select how many optimal locations to find"
    )
    
    qaoa_layers = st.slider(
        "QAOA Circuit Depth",
        min_value=1,
        max_value=3,
        value=2,
        help="Higher depth = better accuracy but slower"
    )
    
    st.subheader("MCDA Weights")
    st.markdown("*Adjust importance of each factor*")
    
    solar_weight = st.slider("☀️ Solar Irradiance", 0.0, 1.0, 0.5, 0.05)
    wind_weight = st.slider("💨 Wind Speed", 0.0, 1.0, 0.3, 0.05)
    risk_weight = st.slider("⚠️ Risk Penalty", 0.0, 1.0, 0.4, 0.05)
    grid_weight = st.slider("📍 Grid Distance Penalty", 0.0, 0.01, 0.001, 0.001)
    
    st.divider()
    
    # Optimize button
    if st.button("🚀 Run Quantum Optimization", use_container_width=True):
        with st.spinner("Running QAOA...This may take 30-60 seconds..."):
            # Calculate suitability scores
            df_scored = calculate_suitability_score(df, solar_weight, wind_weight, risk_weight, grid_weight)
            
            # Prepare data for quantum optimizer
            suitability_scores = df_scored['Suitability_Score'].values
            coordinates = df_scored[['Latitude', 'Longitude']].values
            risk_scores = df_scored['Risk_Score'].values
            
            # Progress placeholder
            progress_text = st.empty()
            
            def update_progress(msg):
                progress_text.info(msg)
            
            # Run quantum optimization
            optimizer = QuantumEnergyOptimizer(
                n_sites_to_select=n_sites,
                qaoa_layers=qaoa_layers
            )
            
            selected_relative, energy = optimizer.optimize(
                suitability_scores,
                coordinates,
                risk_scores,
                progress_callback=update_progress
            )
            
            # Map back to original dataframe indices
            selected_indices = df_scored.index[selected_relative].tolist()
            
            # Store in session state
            st.session_state.optimized = True
            st.session_state.selected_sites = selected_indices
            st.session_state.df_scored = df_scored
            st.session_state.energy = energy
            
            progress_text.success("✅ Optimization Complete!")
            time.sleep(1)
            progress_text.empty()
            st.rerun()
    
    st.divider()
    
    # Export section
    if st.session_state.optimized:
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = export_results(st.session_state.df_scored, st.session_state.selected_sites, 'csv')
            st.download_button(
                label="CSV",
                data=csv_data,
                file_name="optimal_sites.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_data = export_results(st.session_state.df_scored, st.session_state.selected_sites, 'json')
            st.download_button(
                label="JSON",
                data=json_data,
                file_name="optimal_sites.json",
                mime="application/json",
                use_container_width=True
            )

# Main content area
if not st.session_state.optimized:
    # Initial state
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 How It Works
    
    1. **Classical AI Processing**: Multi-Criteria Decision Analysis (MCDA) evaluates each location
    2. **Quantum Optimization**: QAOA algorithm finds optimal site combinations
    3. **Smart Selection**: Balances energy production, safety, and grid resilience
    
    **Configure parameters in the sidebar and click "Run Quantum Optimization" to begin.**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show data preview
    st.subheader("📊 Dataset Overview")
    st.dataframe(df, use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Locations", len(df))
    with col2:
        st.metric("Accessible Sites", len(df[df['Accessibility'] == 1]))
    with col3:
        st.metric("High Risk Zones", len(df[df['Risk_Score'] > 7]))
    
    # Show initial map
    st.subheader("🗺️ Gaza Strip - All Candidate Locations")
    initial_map = create_map(df)
    folium_static(initial_map, width=1400, height=600)
    
else:
    # Results view
    df_scored = st.session_state.df_scored
    selected_sites = st.session_state.selected_sites
    
    st.success(f"✅ Quantum optimization completed! {len(selected_sites)} optimal sites selected.")
    
    # Metrics
    st.subheader("📈 Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    selected_df = df_scored.loc[selected_sites]
    
    total_solar = selected_df['Solar_Irradiance'].sum()
    total_wind = selected_df['Wind_Speed'].sum()
    avg_risk = selected_df['Risk_Score'].mean()
    avg_suitability = selected_df['Suitability_Score'].mean()
    
    with col1:
        st.metric("Total Solar Potential", f"{total_solar:.1f} kWh/m²/day")
    with col2:
        st.metric("Total Wind Potential", f"{total_wind:.1f} m/s")
    with col3:
        st.metric("Average Risk Score", f"{avg_risk:.1f}/10")
    with col4:
        st.metric("Avg Suitability", f"{avg_suitability:.3f}")
    
    # Map with selected sites
    st.subheader("🗺️ Optimal Site Locations")
    result_map = create_map(df_scored, selected_sites)
    folium_static(result_map, width=1400, height=600)
    
    # Selected sites table
    st.subheader("📋 Selected Sites Details")
    display_df = selected_df[[
        'Region_ID', 'Latitude', 'Longitude', 'Solar_Irradiance',
        'Wind_Speed', 'Risk_Score', 'Grid_Distance', 'Suitability_Score'
    ]].copy()
    display_df['Suitability_Score'] = display_df['Suitability_Score'].round(4)
    st.dataframe(display_df, use_container_width=True)
    
    # Analysis
    st.subheader("🔍 Distribution Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Regional Distribution:**")
        region_dist = selected_df['Region_ID'].apply(lambda x: x.split('_')[0] + '_' + x.split('_')[1]).value_counts()
        for region, count in region_dist.items():
            st.write(f"- {region}: {count} site(s)")
    
    with col2:
        st.markdown("**Risk Assessment:**")
        low_risk = len(selected_df[selected_df['Risk_Score'] <= 3])
        med_risk = len(selected_df[(selected_df['Risk_Score'] > 3) & (selected_df['Risk_Score'] <= 7)])
        high_risk = len(selected_df[selected_df['Risk_Score'] > 7])
        st.write(f"- Low Risk (0-3): {low_risk} sites")
        st.write(f"- Medium Risk (4-7): {med_risk} sites")
        st.write(f"- High Risk (8-10): {high_risk} sites")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p><b>GazaGrid Quantum Energy Optimizer</b> | Powered by Qiskit QAOA | Built for Resilience</p>
    <p style="font-size: 0.9rem;">🌍 Optimizing renewable energy for a sustainable future</p>
</div>
""", unsafe_allow_html=True)
