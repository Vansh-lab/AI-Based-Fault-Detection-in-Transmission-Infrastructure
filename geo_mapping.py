"""
Geo Mapping Module
Creates GPS-based mapping for transmission line infrastructure with fault detection visualization.
"""

import pandas as pd
import numpy as np
import folium
from folium import plugins
import os


def generate_corridor_data(num_towers=15, corridor_name="East Region Transmission Line"):
    """
    Generate dummy GPS data for transmission towers along a corridor.
    
    Parameters:
    -----------
    num_towers : int
        Number of towers to generate
    corridor_name : str
        Name of the transmission corridor
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with columns: Image_ID, Latitude, Longitude, Status, Severity
    """
    
    # Define a specific corridor (straight line through a city)
    # Starting point: Downtown area
    start_lat = 28.6139  # Delhi coordinates as example
    start_lon = 77.2090
    
    # End point: suburban area (about 30 km away)
    end_lat = 28.5355
    end_lon = 77.3910
    
    # Generate coordinates along the line
    latitudes = np.linspace(start_lat, end_lat, num_towers)
    longitudes = np.linspace(start_lon, end_lon, num_towers)
    
    # Generate random faults (for demo)
    np.random.seed(42)
    statuses = np.random.choice(['Normal', 'Rusty_Structure', 'Damaged_Insulator'], 
                                 size=num_towers, 
                                 p=[0.6, 0.25, 0.15])
    
    # Generate severity scores based on status
    severities = []
    for status in statuses:
        if status == 'Normal':
            severity = np.random.uniform(0, 5)
        elif status == 'Rusty_Structure':
            severity = np.random.uniform(15, 40)
        else:  # Damaged_Insulator
            severity = np.random.uniform(45, 95)
        severities.append(round(severity, 2))
    
    # Create DataFrame
    data = {
        'Image_ID': [f'Tower_{i+1:03d}' for i in range(num_towers)],
        'Latitude': latitudes,
        'Longitude': longitudes,
        'Status': statuses,
        'Severity': severities,
        'Corridor': corridor_name,
        'Last_Inspected': pd.date_range(start='2026-01-01', periods=num_towers, freq='D')
    }
    
    df = pd.DataFrame(data)
    return df


def get_marker_color(status, severity):
    """
    Determine marker color based on status and severity.
    
    Parameters:
    -----------
    status : str
        Predicted class (Normal, Rusty_Structure, Damaged_Insulator)
    severity : float
        Severity score (0-100)
    
    Returns:
    --------
    str
        Color name for folium marker
    """
    
    if status == 'Normal':
        return 'green'
    elif status == 'Rusty_Structure':
        if severity < 20:
            return 'orange'
        else:
            return 'red'
    elif status == 'Damaged_Insulator':
        if severity < 50:
            return 'orange'
        else:
            return 'red'
    else:
        return 'gray'


def create_transmission_map(df, map_name="transmission_corridor.html"):
    """
    Create an interactive folium map with tower markers.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with tower coordinates and fault data
    map_name : str
        Output filename for the map
    
    Returns:
    --------
    folium.Map
        Interactive map object
    """
    
    # Calculate map center
    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()
    
    # Create map
    transmission_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add title as custom control
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 80px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; font-weight: bold; padding: 10px;
                border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3)">
    <p style="margin: 5px; color: #333;">🌍 Transmission Line Corridor Map</p>
    <p style="margin: 5px; font-size: 12px; color: #666;">Interactive fault detection visualization</p>
    </div>
    '''
    transmission_map.get_root().html.add_child(folium.Element(title_html))
    
    # Add markers for each tower
    for idx, row in df.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        tower_id = row['Image_ID']
        status = row['Status']
        severity = row['Severity']
        last_inspected = row['Last_Inspected'].strftime('%Y-%m-%d')
        
        # Determine marker color
        color = get_marker_color(status, severity)
        
        # Create icon
        if status == 'Normal':
            icon_char = '✓'
            prefix = 'fa'
            icon_name = 'check'
        elif status == 'Rusty_Structure':
            icon_char = '⚠'
            prefix = 'fa'
            icon_name = 'warning'
        else:
            icon_char = '✕'
            prefix = 'fa'
            icon_name = 'times'
        
        # Create popup content
        popup_text = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin: 5px; color: #333;">{tower_id}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px;"><b>Status:</b> {status}</p>
            <p style="margin: 5px;"><b>Severity:</b> {severity}%</p>
            <p style="margin: 5px;"><b>Latitude:</b> {lat:.6f}</p>
            <p style="margin: 5px;"><b>Longitude:</b> {lon:.6f}</p>
            <p style="margin: 5px;"><b>Last Inspected:</b> {last_inspected}</p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px; font-size: 12px; color: #666;">
                Click on map for more details
            </p>
        </div>
        """
        
        # Add marker with popup and tooltip
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=f"{tower_id} - {status}",
            icon=folium.Icon(
                color=color,
                icon=icon_name,
                prefix=prefix,
                icon_color='white'
            )
        ).add_to(transmission_map)
    
    # Add a legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 10px; width: 220px; height: 220px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px;
                border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3)">
    <p style="margin: 0 0 10px 0; font-weight: bold; color: #333;">Legend</p>
    <p style="margin: 5px 0;">
        <i class="fa fa-map-marker" style="color:green"></i> 
        <span>Normal (0-10%)</span>
    </p>
    <p style="margin: 5px 0;">
        <i class="fa fa-map-marker" style="color:orange"></i> 
        <span>Medium Severity (10-40%)</span>
    </p>
    <p style="margin: 5px 0;">
        <i class="fa fa-map-marker" style="color:red"></i> 
        <span>Critical (>40%)</span>
    </p>
    <hr style="margin: 10px 0;">
    <p style="margin: 5px 0; font-size: 12px; color: #666;">
        <b>Fault Types:</b>
    </p>
    <p style="margin: 3px 0; font-size: 11px;">
        ✓ Normal - No issues
    </p>
    <p style="margin: 3px 0; font-size: 11px;">
        ⚠ Rusty - Corrosion detected
    </p>
    <p style="margin: 3px 0; font-size: 11px;">
        ✕ Damaged - Component damage
    </p>
    </div>
    '''
    transmission_map.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control for different map styles
    folium.TileLayer('CartoDB positron').add_to(transmission_map)
    folium.TileLayer('CartoDB voyager').add_to(transmission_map)
    folium.LayerControl().add_to(transmission_map)
    
    # Add draw tools for corridor visualization
    # Draw a line connecting the towers
    tower_coords = df[['Latitude', 'Longitude']].values.tolist()
    folium.PolyLine(
        locations=tower_coords,
        color='blue',
        weight=2,
        opacity=0.6,
        popup='Transmission Corridor'
    ).add_to(transmission_map)
    
    # Save map
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    map_path = os.path.join(templates_dir, map_name)
    transmission_map.save(map_path)
    print(f"✓ Map saved to: {map_path}")
    
    return transmission_map


def create_severity_heatmap(df, map_name="severity_heatmap.html"):
    """
    Create a heatmap visualization of severity across the corridor.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with tower coordinates and severity data
    map_name : str
        Output filename for the map
    
    Returns:
    --------
    folium.Map
        Heatmap visualization
    """
    
    # Calculate map center
    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()
    
    # Create map
    heatmap = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Prepare data for heatmap (latitude, longitude, severity)
    heat_data = [[row['Latitude'], row['Longitude'], row['Severity']] 
                 for idx, row in df.iterrows()]
    
    # Add heatmap layer
    plugins.HeatMap(heat_data, radius=30, blur=25, max_zoom=15).add_to(heatmap)
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 80px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; font-weight: bold; padding: 10px;
                border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3)">
    <p style="margin: 5px; color: #333;">🔥 Severity Heatmap</p>
    <p style="margin: 5px; font-size: 12px; color: #666;">Red = High severity, Blue = Low severity</p>
    </div>
    '''
    heatmap.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    map_path = os.path.join(templates_dir, map_name)
    heatmap.save(map_path)
    print(f"✓ Heatmap saved to: {map_path}")
    
    return heatmap


def generate_corridor_report(df):
    """
    Generate a statistical report of the corridor.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with tower data
    
    Returns:
    --------
    dict
        Report with statistics
    """
    
    total_towers = len(df)
    normal_towers = len(df[df['Status'] == 'Normal'])
    rusty_towers = len(df[df['Status'] == 'Rusty_Structure'])
    damaged_towers = len(df[df['Status'] == 'Damaged_Insulator'])
    
    critical_towers = len(df[df['Severity'] > 40])
    medium_towers = len(df[(df['Severity'] >= 10) & (df['Severity'] <= 40)])
    
    avg_severity = df['Severity'].mean()
    max_severity = df['Severity'].max()
    
    report = {
        'total_towers': total_towers,
        'normal_towers': normal_towers,
        'rusty_towers': rusty_towers,
        'damaged_towers': damaged_towers,
        'critical_towers': critical_towers,
        'medium_severity_towers': medium_towers,
        'average_severity': round(avg_severity, 2),
        'max_severity': round(max_severity, 2),
        'status_percentages': {
            'Normal': round((normal_towers / total_towers) * 100, 2),
            'Rusty': round((rusty_towers / total_towers) * 100, 2),
            'Damaged': round((damaged_towers / total_towers) * 100, 2)
        },
        'maintenance_required': {
            'Critical': critical_towers,
            'Medium': medium_towers,
            'Low': normal_towers
        }
    }
    
    return report


if __name__ == "__main__":
    print("Generating sample transmission corridor data...")
    
    # Generate dummy data
    corridor_df = generate_corridor_data(num_towers=20)
    print(f"\n✓ Generated data for {len(corridor_df)} towers")
    print("\nSample data:")
    print(corridor_df.head())
    
    # Generate report
    report = generate_corridor_report(corridor_df)
    print("\n" + "="*60)
    print("CORRIDOR INSPECTION REPORT")
    print("="*60)
    print(f"Total Towers: {report['total_towers']}")
    print(f"Normal Towers: {report['normal_towers']} ({report['status_percentages']['Normal']}%)")
    print(f"Rusty Towers: {report['rusty_towers']} ({report['status_percentages']['Rusty']}%)")
    print(f"Damaged Towers: {report['damaged_towers']} ({report['status_percentages']['Damaged']}%)")
    print(f"\nCritical (Immediate Action): {report['maintenance_required']['Critical']} towers")
    print(f"Medium (Plan Maintenance): {report['maintenance_required']['Medium']} towers")
    print(f"Low (Monitor): {report['maintenance_required']['Low']} towers")
    print(f"\nAverage Severity: {report['average_severity']}%")
    print(f"Maximum Severity: {report['max_severity']}%")
    print("="*60)
    
    # Create maps
    print("\nCreating interactive maps...")
    create_transmission_map(corridor_df)
    create_severity_heatmap(corridor_df)
    print("✓ Maps created successfully!")
