"""
Severity Analyzer Module
Quantifies fault severity using image segmentation and color space analysis.
"""

import cv2
import numpy as np
from PIL import Image


def calculate_severity(image_path, prediction_class):
    """
    Calculate the severity level of detected fault.
    
    Parameters:
    -----------
    image_path : str or numpy.ndarray
        Path to image or image array
    prediction_class : str
        Predicted class (Normal, Rusty_Structure, Damaged_Insulator)
    
    Returns:
    --------
    dict
        Dictionary containing severity_score, severity_category, and masked_image
    
    Logic:
    ------
    - For 'Normal' class: Return 0% (no fault)
    - For 'Rusty_Structure' or 'Damaged_Insulator':
        * Convert to HSV color space
        * Create mask for rust/damage (brown/orange colors)
        * Calculate percentage of affected area
        * Categorize as Low/Medium/Critical
    """
    
    # Load image if path is provided
    if isinstance(image_path, str):
        image = cv2.imread(image_path)
        if image is None:
            return {
                'severity_score': 0,
                'severity_category': 'Unknown',
                'masked_image': None,
                'error': 'Could not load image'
            }
    else:
        image = image_path
    
    # If Normal, return 0% severity
    if prediction_class == 'Normal':
        return {
            'severity_score': 0.0,
            'severity_category': 'Low (Monitor)',
            'masked_image': image,
            'defect_pixels': 0,
            'total_pixels': image.shape[0] * image.shape[1]
        }
    
    # Convert to HSV for better color detection
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # ============= RUST DETECTION (Brown/Orange Colors) =============
    # Define lower and upper bounds for rust colors in HSV
    # Orange/Brown hue range: 5-25 (OpenCV HSV: 0-180)
    lower_rust_1 = np.array([5, 100, 100])
    upper_rust_1 = np.array([25, 255, 255])
    
    # Light orange for lighter rust areas
    lower_rust_2 = np.array([0, 80, 80])
    upper_rust_2 = np.array([20, 200, 220])
    
    # Create masks for rust colors
    mask_rust_1 = cv2.inRange(hsv_image, lower_rust_1, upper_rust_1)
    mask_rust_2 = cv2.inRange(hsv_image, lower_rust_2, upper_rust_2)
    
    # Combine masks
    rust_mask = cv2.bitwise_or(mask_rust_1, mask_rust_2)
    
    # ============= DAMAGE DETECTION (Dark regions, sharp edges) =============
    # Convert to grayscale for edge detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, 50, 150)
    
    # Apply morphological operations to enhance damage regions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    
    # Combine rust mask with damage edges
    combined_mask = cv2.bitwise_or(rust_mask, dilated_edges)
    
    # Apply morphological closing to fill small gaps
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel_close)
    
    # ============= CALCULATE SEVERITY SCORE =============
    # Count defective pixels (non-zero pixels in mask)
    defect_pixels = np.count_nonzero(combined_mask)
    
    # Total pixels in image
    total_pixels = image.shape[0] * image.shape[1]
    
    # Calculate severity percentage
    severity_score = (defect_pixels / total_pixels) * 100
    
    # Ensure score is within 0-100 range
    severity_score = min(severity_score, 100.0)
    severity_score = max(severity_score, 0.0)
    
    # ============= CATEGORIZE SEVERITY =============
    if severity_score < 10:
        severity_category = "Low (Monitor)"
    elif severity_score < 40:
        severity_category = "Medium (Plan Maintenance)"
    else:
        severity_category = "CRITICAL (Immediate Action)"
    
    # Create visualization: overlay mask on original image
    masked_image = image.copy()
    masked_image[combined_mask > 0] = [0, 0, 255]  # Red color for defects
    
    return {
        'severity_score': round(severity_score, 2),
        'severity_category': severity_category,
        'masked_image': masked_image,
        'defect_pixels': defect_pixels,
        'total_pixels': total_pixels,
        'raw_mask': combined_mask
    }


def get_severity_color(severity_category):
    """
    Get color based on severity category for visualization.
    
    Parameters:
    -----------
    severity_category : str
        Severity category string
    
    Returns:
    --------
    tuple
        (R, G, B) color tuple
    """
    
    if "Low" in severity_category:
        return (144, 238, 144)  # Light green
    elif "Medium" in severity_category:
        return (255, 165, 0)    # Orange
    elif "CRITICAL" in severity_category:
        return (255, 0, 0)      # Red
    else:
        return (200, 200, 200)  # Gray


def calculate_affected_area_bbox(mask):
    """
    Calculate the bounding box of the most affected area.
    
    Parameters:
    -----------
    mask : numpy.ndarray
        Binary mask of defect region
    
    Returns:
    --------
    tuple
        (x, y, width, height) of bounding box
    """
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return (0, 0, 0, 0)
    
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    return (x, y, w, h)


def analyze_damage_distribution(mask, image_shape):
    """
    Analyze the distribution of damage across the image regions.
    
    Parameters:
    -----------
    mask : numpy.ndarray
        Binary mask of defect region
    image_shape : tuple
        Shape of original image
    
    Returns:
    --------
    dict
        Distribution metrics
    """
    
    height, width = image_shape[:2]
    
    # Divide image into 9 regions (3x3 grid)
    region_height = height // 3
    region_width = width // 3
    
    damage_by_region = {}
    
    regions = {
        'top_left': (0, 0, region_width, region_height),
        'top_center': (region_width, 0, 2*region_width, region_height),
        'top_right': (2*region_width, 0, width, region_height),
        'middle_left': (0, region_height, region_width, 2*region_height),
        'middle_center': (region_width, region_height, 2*region_width, 2*region_height),
        'middle_right': (2*region_width, region_height, width, 2*region_height),
        'bottom_left': (0, 2*region_height, region_width, height),
        'bottom_center': (region_width, 2*region_height, 2*region_width, height),
        'bottom_right': (2*region_width, 2*region_height, width, height)
    }
    
    for region_name, (x1, y1, x2, y2) in regions.items():
        region_mask = mask[y1:y2, x1:x2]
        damage_percentage = (np.count_nonzero(region_mask) / (region_mask.shape[0] * region_mask.shape[1])) * 100
        damage_by_region[region_name] = round(damage_percentage, 2)
    
    return damage_by_region


if __name__ == "__main__":
    print("Severity Analyzer Module Loaded Successfully!")
    print("\nUsage:")
    print("from severity_analyzer import calculate_severity")
    print("severity = calculate_severity('image.jpg', 'Rusty_Structure')")
    print(f"Score: {severity['severity_score']}%")
    print(f"Category: {severity['severity_category']}")
