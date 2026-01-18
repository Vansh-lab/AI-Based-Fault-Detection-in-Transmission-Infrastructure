"""
Grad-CAM (Gradient-weighted Class Activation Mapping) Module
Provides model explainability by visualizing important regions in images for predictions.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import models
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def generate_grad_cam(model, image_array, class_index, layer_name='block_16_expand_relu'):
    """
    Generates Grad-CAM heatmap for a given image and class.
    
    Grad-CAM (Gradient-weighted Class Activation Mapping) shows which regions
    of the image were important for the model's prediction.
    
    Parameters:
    -----------
    model : keras.Model
        The trained neural network model
    image_array : np.ndarray
        Input image as numpy array (224, 224, 3) normalized to [0, 1]
    class_index : int
        Index of the target class for which to generate CAM
    layer_name : str
        Name of the layer to use for gradient computation (default: last convolution layer)
    
    Returns:
    --------
    heatmap : np.ndarray
        Grad-CAM heatmap normalized to [0, 1]
    """
    
    # Create a model that outputs both the predictions and the activations
    # from the specified convolutional layer
    grad_model = models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output]
    )
    
    # Convert input to tensor for gradient computation
    image_tensor = tf.convert_to_tensor(image_array[np.newaxis, ...], dtype=tf.float32)
    
    # Use GradientTape to compute gradients
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image_tensor)
        loss = predictions[:, class_index]
    
    # Compute gradients of the loss with respect to convolution outputs
    grads = tape.gradient(loss, conv_outputs)
    
    # Compute the weights for each channel (average pooling over spatial dimensions)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Compute the weighted sum of feature maps
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(pooled_grads[..., tf.newaxis] * conv_outputs, axis=-1)
    
    # Normalize heatmap to [0, 1]
    heatmap = tf.nn.relu(heatmap)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    
    return heatmap.numpy()


def overlay_heatmap_on_image(original_image, heatmap, alpha=0.4, colormap='jet'):
    """
    Overlays the Grad-CAM heatmap on the original image.
    
    Parameters:
    -----------
    original_image : np.ndarray or PIL.Image
        Original input image (H, W, 3) in range [0, 255] or [0, 1]
    heatmap : np.ndarray
        Grad-CAM heatmap (H, W) in range [0, 1]
    alpha : float
        Transparency of heatmap overlay (0.0 to 1.0)
    colormap : str
        Matplotlib colormap name (default: 'jet')
    
    Returns:
    --------
    overlay_image : np.ndarray
        Image with heatmap overlay (H, W, 3) in range [0, 255]
    """
    
    # Convert PIL Image to numpy if needed
    if isinstance(original_image, Image.Image):
        original_image = np.array(original_image)
    
    # Ensure image is in [0, 255] range
    if original_image.max() <= 1.0:
        original_image = (original_image * 255).astype(np.uint8)
    else:
        original_image = original_image.astype(np.uint8)
    
    # Resize heatmap to match original image size
    h, w = original_image.shape[:2]
    heatmap_resized = cv2.resize(heatmap, (w, h))
    
    # Apply colormap to heatmap
    cmap = cm.get_cmap(colormap)
    heatmap_colored = cmap(heatmap_resized)[:, :, :3]  # Remove alpha channel
    heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
    
    # Convert original image to float for blending
    original_float = original_image.astype(np.float32)
    heatmap_float = heatmap_colored.astype(np.float32)
    
    # Blend images
    overlay = (alpha * heatmap_float + (1 - alpha) * original_float).astype(np.uint8)
    
    return overlay


def visualize_prediction_with_gradcam(image_path, model, class_names, 
                                      layer_name='block_16_expand_relu',
                                      image_size=(224, 224)):
    """
    Complete visualization function: prediction + Grad-CAM overlay.
    
    Parameters:
    -----------
    image_path : str
        Path to the input image
    model : keras.Model
        Trained model
    class_names : list
        List of class names
    layer_name : str
        Convolutional layer name for Grad-CAM
    image_size : tuple
        Target image size
    
    Returns:
    --------
    dict
        Dictionary containing prediction info and visualizations
    """
    
    # Load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img_resized = img.resize(image_size)
    img_array = np.array(img_resized) / 255.0  # Normalize to [0, 1]
    
    # Get model prediction
    predictions = model.predict(img_array[np.newaxis, ...], verbose=0)
    class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][class_index])
    predicted_class = class_names[class_index]
    
    # Generate Grad-CAM
    heatmap = generate_grad_cam(model, img_array, class_index, layer_name)
    
    # Create overlay
    overlay = overlay_heatmap_on_image(img_resized, heatmap, alpha=0.5, colormap='jet')
    
    return {
        'original_image': np.array(img_resized),
        'heatmap': heatmap,
        'overlay': overlay,
        'predicted_class': predicted_class,
        'confidence': confidence,
        'all_predictions': {class_names[i]: float(predictions[0][i]) 
                           for i in range(len(class_names))}
    }


def plot_grad_cam_results(results, save_path=None):
    """
    Plots original image, heatmap, and overlay side by side.
    
    Parameters:
    -----------
    results : dict
        Results dictionary from visualize_prediction_with_gradcam
    save_path : str, optional
        Path to save the figure
    """
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original Image
    axes[0].imshow(results['original_image'].astype(np.uint8))
    axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    # Heatmap
    im = axes[1].imshow(results['heatmap'], cmap='jet')
    axes[1].set_title('Grad-CAM Heatmap', fontsize=12, fontweight='bold')
    axes[1].axis('off')
    plt.colorbar(im, ax=axes[1])
    
    # Overlay
    axes[2].imshow(results['overlay'])
    axes[2].set_title('Heatmap Overlay', fontsize=12, fontweight='bold')
    axes[2].axis('off')
    
    # Add prediction info
    title_text = f"Predicted: {results['predicted_class']}\nConfidence: {results['confidence']*100:.2f}%"
    fig.suptitle(title_text, fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Grad-CAM visualization saved to: {save_path}")
    
    plt.show()


if __name__ == "__main__":
    # Example usage (requires trained model)
    print("Grad-CAM Module Loaded Successfully!")
    print("\nUsage:")
    print("1. from grad_cam import visualize_prediction_with_gradcam")
    print("2. results = visualize_prediction_with_gradcam(image_path, model, class_names)")
    print("3. plot_grad_cam_results(results)")
