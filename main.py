"""
Streamlit Web Application for Transmission Line Fault Detection
Interactive dashboard for real-time fault detection and visualization with severity analysis and geospatial mapping.
"""

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from pathlib import Path
import sys
import os
import warnings
import pandas as pd
import folium
from streamlit_folium import st_folium

warnings.filterwarnings('ignore')

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    from grad_cam import visualize_prediction_with_gradcam, overlay_heatmap_on_image
except ImportError:
    st.warning("Grad-CAM module not found. Some features may be limited.")

try:
    from severity_analyzer import calculate_severity, get_severity_color
except ImportError:
    st.warning("Severity analyzer module not found. Severity analysis unavailable.")

try:
    from geo_mapping import (generate_corridor_data, create_transmission_map, 
                             create_severity_heatmap, generate_corridor_report)
except ImportError:
    st.warning("Geo-mapping module not found. Map features unavailable.")


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Transmission Line Fault Detector",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #28a745;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_resource
def load_model(model_path):
    """
    Load the pre-trained CNN model.
    Uses caching to load the model only once.
    """
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


def get_model_layer_name(model):
    """
    Dynamically find the last convolutional layer in the model.
    """
    for layer in reversed(model.layers):
        if 'conv' in layer.name.lower() or 'expand' in layer.name.lower():
            return layer.name
    return None


def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess image for model prediction.
    """
    img_resized = image.resize(target_size)
    img_array = np.array(img_resized) / 255.0
    return img_array


def predict_fault(model, image_array, class_names):
    """
    Make prediction on the input image.
    """
    predictions = model.predict(image_array[np.newaxis, ...], verbose=0)
    class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][class_index])
    predicted_class = class_names[class_index]
    
    return {
        'class': predicted_class,
        'confidence': confidence,
        'all_scores': {class_names[i]: float(predictions[0][i]) 
                      for i in range(len(class_names))}
    }


def is_fault_detected(predicted_class):
    """
    Determine if a fault is detected based on prediction.
    """
    fault_classes = ['Rusty_Tower', 'Damaged_Insulator']
    return predicted_class in fault_classes


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown('<div class="title-text">⚡ AI-Powered Transmission Line Fault Detector</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Intelligent CNN-based system for predictive maintenance</div>', 
                unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model path configuration
        model_dir = Path(__file__).parent.parent / "models"
        model_path = model_dir / "fault_detector_best.h5"
        
        st.info(f"Model Path: `{model_path}`")
        
        # Class names (should match your dataset)
        class_names = ['Normal', 'Rusty_Tower', 'Damaged_Insulator']
        st.write("**Expected Classes:**")
        for idx, class_name in enumerate(class_names):
            st.write(f"  {idx+1}. {class_name}")
    
    # Load model
    st.info("🔄 Loading model...")
    model_dir = Path(__file__).parent.parent / "models"
    model_path = model_dir / "fault_detector_best.h5"
    
    model = load_model(str(model_path))
    
    if model is None:
        st.error("""
        ❌ **Model not found!**
        
        Please ensure:
        1. The model has been trained and saved to `models/fault_detector_best.h5`
        2. Run `python src/train.py` from the project root directory
        """)
        return
    
    st.success("✓ Model loaded successfully!")
    
    # Class names
    class_names = ['Normal', 'Rusty_Tower', 'Damaged_Insulator']
    
    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.header("📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Upload a transmission line image (JPG/PNG)",
            type=['jpg', 'jpeg', 'png']
        )
        
        if uploaded_file is not None:
            # Load and display image
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Preprocess image
            preprocessed_image = preprocess_image(image)
            
            # Make prediction
            st.info("🔍 Analyzing image...")
            prediction = predict_fault(model, preprocessed_image, class_names)
            
            # Save temporary image for severity analysis
            temp_image_path = "/tmp/temp_image.jpg"
            image.save(temp_image_path)
            
            # Calculate severity
            severity_result = None
            try:
                severity_result = calculate_severity(temp_image_path, prediction['class'])
            except Exception as e:
                st.warning(f"Severity analysis unavailable: {str(e)}")
            
            # Display prediction
            st.success("✓ Analysis complete!")
            
            with col2:
                st.header("📊 Prediction Results")
                
                # Main prediction
                st.metric(
                    label="Predicted Class",
                    value=prediction['class'],
                    delta=f"{prediction['confidence']*100:.2f}% Confidence"
                )
                
                # Confidence scores for all classes
                st.subheader("Confidence Scores")
                for class_name, score in prediction['all_scores'].items():
                    col_name, col_bar = st.columns([1, 3])
                    with col_name:
                        st.write(f"**{class_name}**")
                    with col_bar:
                        st.progress(min(score, 1.0))
                    st.write(f"  {score*100:.2f}%")
                
                # Fault detection alert
                st.subheader("⚠️ Alert Status")
                if is_fault_detected(prediction['class']):
                    st.markdown(
                        '<div class="warning-box">'
                        '<h3>⚠️ MAINTENANCE REQUIRED</h3>'
                        '<p>Fault detected in transmission line. Immediate maintenance recommended.</p>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div class="success-box">'
                        '<h3>✅ NO FAULT DETECTED</h3>'
                        '<p>Transmission line is in normal operating condition.</p>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                
                # Severity Analysis Section
                if severity_result:
                    st.subheader("🔴 Fault Severity Analysis")
                    
                    severity_score = severity_result['severity_score']
                    severity_category = severity_result['severity_category']
                    
                    # Display severity progress bar
                    col_sev1, col_sev2 = st.columns([3, 1])
                    with col_sev1:
                        st.progress(min(severity_score / 100, 1.0))
                    with col_sev2:
                        st.metric("Severity", f"{severity_score:.1f}%")
                    
                    # Display severity category with color
                    severity_color = get_severity_color(severity_category)
                    color_hex = f'#{int(severity_color[0]*255):02x}{int(severity_color[1]*255):02x}{int(severity_color[2]*255):02x}'
                    
                    st.markdown(f"""
                    <div style='background-color: {color_hex}30; border: 2px solid {color_hex}; 
                                border-radius: 5px; padding: 1rem; margin: 1rem 0;'>
                    <h4 style='color: {color_hex};'>Status: {severity_category}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show critical warning if needed
                    if severity_score > 40:
                        st.error(f"""
                        🚨 **CRITICAL - IMMEDIATE ACTION REQUIRED**
                        
                        This component has {severity_score:.1f}% damage/degradation and requires immediate maintenance.
                        Please schedule emergency inspection and repair operations.
                        """)
                    elif severity_score > 10:
                        st.warning(f"""
                        ⚠️ **Medium Severity - Plan Maintenance**
                        
                        This component shows {severity_score:.1f}% fault signs. Schedule maintenance within 30 days.
                        """)
                    else:
                        st.info(f"""
                        📋 **Low Severity - Monitor**
                        
                        Minor issues detected ({severity_score:.1f}%). Continue regular monitoring.
                        """)
                    
                    # Display masked image showing defects
                    if 'masked_image' in severity_result:
                        st.image(severity_result['masked_image'], 
                                caption="Defect Regions (Red Overlay)", use_column_width=True)
            
            # Grad-CAM Visualization (Advanced Feature)
            st.header("🔬 Model Explainability (Grad-CAM)")
            st.write("""
            Grad-CAM (Gradient-weighted Class Activation Mapping) shows which regions 
            of the image the model focused on for its prediction.
            """)
            
            try:
                # Get the convolutional layer name
                conv_layer = get_model_layer_name(model)
                
                if conv_layer:
                    st.info(f"Generating Grad-CAM visualization using layer: `{conv_layer}`")
                    
                    # Generate Grad-CAM
                    results = visualize_prediction_with_gradcam(
                        uploaded_file.name,
                        model,
                        class_names,
                        layer_name=conv_layer,
                        image_size=(224, 224)
                    )
                    
                    # Display Grad-CAM results
                    grad_col1, grad_col2, grad_col3 = st.columns(3)
                    
                    with grad_col1:
                        st.image(results['original_image'], 
                                caption="Original Image", use_column_width=True)
                    
                    with grad_col2:
                        st.image(results['heatmap'], 
                                caption="Grad-CAM Heatmap", use_column_width=True)
                    
                    with grad_col3:
                        st.image(results['overlay'], 
                                caption="Heatmap Overlay", use_column_width=True)
                    
                    st.success("✓ Grad-CAM visualization generated successfully!")
                    st.write("""
                    **Interpretation:**
                    - Red/Warm colors: High activation (important regions)
                    - Blue/Cool colors: Low activation (less important regions)
                    """)
                else:
                    st.warning("Could not identify convolutional layer for Grad-CAM")
                    
            except Exception as e:
                st.warning(f"Grad-CAM visualization unavailable: {str(e)}")
        
        else:
            # Display placeholder
            with col2:
                st.header("📊 Prediction Results")
                st.info("👆 Upload an image to see predictions and analysis")
    
    # ========================================================================
    # GEOSPATIAL MAPPING SECTION
    # ========================================================================
    st.header("🌍 Transmission Line Corridor Map")
    st.write("""
    This section displays an interactive map of transmission towers with their fault status
    and severity levels. Use the map to visualize faults across the entire corridor.
    """)
    
    # Create two tabs: Interactive Map and Report
    map_tab1, map_tab2 = st.tabs(["📍 Interactive Map", "📈 Corridor Report"])
    
    with map_tab1:
        # Generate corridor data
        try:
            corridor_data = generate_corridor_data(num_towers=20)
            
            # Create the transmission map
            center_lat = corridor_data['Latitude'].mean()
            center_lon = corridor_data['Longitude'].mean()
            
            transmission_map = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Import marker color function
            from geo_mapping import get_marker_color
            
            # Add markers for each tower
            for idx, row in corridor_data.iterrows():
                lat = row['Latitude']
                lon = row['Longitude']
                tower_id = row['Image_ID']
                status = row['Status']
                severity = row['Severity']
                last_inspected = row['Last_Inspected'].strftime('%Y-%m-%d')
                
                color = get_marker_color(status, severity)
                
                popup_text = f"""
                <div style="font-family: Arial; width: 250px;">
                    <h4 style="margin: 5px; color: #333;">{tower_id}</h4>
                    <hr style="margin: 5px 0;">
                    <p style="margin: 5px;"><b>Status:</b> {status}</p>
                    <p style="margin: 5px;"><b>Severity:</b> {severity}%</p>
                    <p style="margin: 5px;"><b>Latitude:</b> {lat:.6f}</p>
                    <p style="margin: 5px;"><b>Longitude:</b> {lon:.6f}</p>
                    <p style="margin: 5px;"><b>Last Inspected:</b> {last_inspected}</p>
                </div>
                """
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"{tower_id} - {status}",
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(transmission_map)
            
            # Add corridor line
            tower_coords = corridor_data[['Latitude', 'Longitude']].values.tolist()
            folium.PolyLine(
                locations=tower_coords,
                color='blue',
                weight=2,
                opacity=0.6,
                popup='Transmission Corridor'
            ).add_to(transmission_map)
            
            # Add legend
            legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; right: 10px; width: 220px; height: 200px; 
                        background-color: white; border:2px solid grey; z-index:9999; 
                        font-size:14px; padding: 10px;
                        border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3)">
            <p style="margin: 0 0 10px 0; font-weight: bold; color: #333;">Legend</p>
            <p style="margin: 5px 0;">
                <i class="fa fa-map-marker" style="color:green"></i> 
                <span>Normal</span>
            </p>
            <p style="margin: 5px 0;">
                <i class="fa fa-map-marker" style="color:orange"></i> 
                <span>Medium Severity</span>
            </p>
            <p style="margin: 5px 0;">
                <i class="fa fa-map-marker" style="color:red"></i> 
                <span>Critical</span>
            </p>
            </div>
            '''
            transmission_map.get_root().html.add_child(folium.Element(legend_html))
            
            # Display map
            st_folium(transmission_map, width=st.session_state.get('map_width', 1200), height=600)
            
        except Exception as e:
            st.error(f"Error creating map: {str(e)}")
    
    with map_tab2:
        # Generate and display corridor report
        try:
            corridor_data = generate_corridor_data(num_towers=20)
            report = generate_corridor_report(corridor_data)
            
            # Display report metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Towers", report['total_towers'])
            with col2:
                st.metric("Normal", report['normal_towers'], 
                         delta=f"{report['status_percentages']['Normal']:.1f}%")
            with col3:
                st.metric("Rusty", report['rusty_towers'],
                         delta=f"{report['status_percentages']['Rusty']:.1f}%")
            with col4:
                st.metric("Damaged", report['damaged_towers'],
                         delta=f"{report['status_percentages']['Damaged']:.1f}%")
            
            st.divider()
            
            # Maintenance schedule
            col_maint1, col_maint2, col_maint3 = st.columns(3)
            
            with col_maint1:
                st.error(f"""
                🚨 **Critical - Immediate Action**
                
                {report['maintenance_required']['Critical']} towers require emergency maintenance
                """)
            
            with col_maint2:
                st.warning(f"""
                ⚠️ **Medium - Plan Maintenance**
                
                {report['maintenance_required']['Medium']} towers need scheduled maintenance
                """)
            
            with col_maint3:
                st.info(f"""
                📋 **Low - Monitor**
                
                {report['maintenance_required']['Low']} towers in normal condition
                """)
            
            st.divider()
            
            # Severity statistics
            st.subheader("📊 Severity Statistics")
            col_avg, col_max = st.columns(2)
            with col_avg:
                st.metric("Average Severity", f"{report['average_severity']}%")
            with col_max:
                st.metric("Maximum Severity", f"{report['max_severity']}%")
            
            # Display data table
            st.subheader("📋 Tower Details")
            st.dataframe(
                corridor_data[[
                    'Image_ID', 'Status', 'Severity', 'Latitude', 'Longitude', 'Last_Inspected'
                ]].sort_values('Severity', ascending=False),
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><b>AI-Based Fault Detection System for Transmission Lines</b></p>
        <p>Powered by Deep Learning (MobileNetV2 Transfer Learning)</p>
        <p>For maintenance and operational support only</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
