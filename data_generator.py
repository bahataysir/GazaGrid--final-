import pandas as pd
import numpy as np
import random

def generate_gaza_energy_data(num_points=45):
    """
    Generate synthetic but realistic energy data for Gaza Strip grid points.
    Gaza coordinates: ~31.25°N-31.58°N, 34.20°E-34.55°E
    """
    np.random.seed(42)
    random.seed(42)
    
    # Gaza regions for realistic naming
    regions = ["North_Gaza", "Gaza_City", "Deir_al_Balah", "Khan_Younis", "Rafah"]
    
    data = []
    
    for i in range(num_points):
        # Distribute points across Gaza Strip
        lat = np.random.uniform(31.25, 31.58)
        lon = np.random.uniform(34.20, 34.55)
        
        # Coastal areas (lon < 34.30) have higher wind speeds
        is_coastal = lon < 34.35
        
        # Solar irradiance (kWh/m²/day) - Gaza has excellent solar potential
        solar_irradiance = np.random.uniform(4.5, 6.0)
        
        # Wind speed (m/s) - Higher near coast
        if is_coastal:
            wind_speed = np.random.uniform(4.0, 6.5)
        else:
            wind_speed = np.random.uniform(2.5, 4.5)
        
        # Risk score (0-10) - Northern areas and border zones higher risk
        # North and South (borders) have higher risk
        if lat > 31.50 or lat < 31.30:
            risk_score = np.random.randint(6, 11)
        else:
            risk_score = np.random.randint(2, 8)
        
        # Accessibility (0/1) - Some areas restricted due to buffer zones
        # ~20% of locations are inaccessible
        accessibility = 1 if np.random.random() > 0.2 else 0
        
        # Grid distance (meters) - Distance to nearest existing power grid node
        grid_distance = np.random.randint(100, 5000)
        
        # Region selection based on latitude
        if lat > 31.50:
            region = "North_Gaza"
        elif lat > 31.45:
            region = "Gaza_City"
        elif lat > 31.38:
            region = "Deir_al_Balah"
        elif lat > 31.30:
            region = "Khan_Younis"
        else:
            region = "Rafah"
        
        data.append({
            'Region_ID': f"{region}_{i:02d}",
            'Latitude': round(lat, 6),
            'Longitude': round(lon, 6),
            'Solar_Irradiance': round(solar_irradiance, 2),
            'Wind_Speed': round(wind_speed, 2),
            'Risk_Score': risk_score,
            'Accessibility': accessibility,
            'Grid_Distance': grid_distance
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Generate data
    df = generate_gaza_energy_data(45)
    
    # Save to CSV
    output_path = "/app/gazagrid/gaza_energy_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df)} data points")
    print(f"✅ Saved to {output_path}")
    print(f"\n📊 Data Summary:")
    print(df.describe())
    print(f"\n🔍 Sample data:")
    print(df.head())
