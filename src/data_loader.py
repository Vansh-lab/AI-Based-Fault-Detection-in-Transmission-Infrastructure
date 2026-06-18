"""
Data Loader Module with Augmentation Pipeline
Provides robust data augmentation for training and preprocessing for validation/test data.
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os


def get_data_generators(data_dir, image_size=(224, 224), batch_size=32):
    """
    Creates and returns data generators for training and validation with augmentation.
    
    Parameters:
    -----------
    data_dir : str
        Path to the dataset directory containing 'train' and 'val' subdirectories
    image_size : tuple
        Target image size (height, width). Default: (224, 224)
    batch_size : int
        Batch size for data loading. Default: 32
    
    Returns:
    --------
    tuple
        (train_generator, validation_generator) for training and validation
    
    Example:
    --------
    >>> train_gen, val_gen = get_data_generators('dataset/')
    >>> # Use with model.fit(train_gen, validation_data=val_gen, ...)
    """
    
    # Training Data Generator with Augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,              # Normalize pixel values to [0, 1]
        rotation_range=20,           # Random rotation up to 20 degrees
        width_shift_range=0.2,       # Random width shift up to 20%
        height_shift_range=0.2,      # Random height shift up to 20%
        zoom_range=0.2,              # Random zoom 0.8x to 1.2x
        horizontal_flip=True,        # Random horizontal flip
        fill_mode='nearest'          # Fill mode for new pixels
    )
    
    # Validation/Test Data Generator (No Augmentation, only Rescaling)
    val_test_datagen = ImageDataGenerator(
        rescale=1./255               # Only normalize, no augmentation
    )
    
    # Load Training Data
    train_path = os.path.join(data_dir, 'train')
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',    # Multi-class classification
        shuffle=True
    )
    
    # Load Validation Data
    val_path = os.path.join(data_dir, 'val')
    validation_generator = val_test_datagen.flow_from_directory(
        val_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, validation_generator


def get_test_generator(data_dir, image_size=(224, 224), batch_size=32):
    """
    Creates and returns test data generator (without augmentation).
    
    Parameters:
    -----------
    data_dir : str
        Path to the dataset directory
    image_size : tuple
        Target image size (height, width). Default: (224, 224)
    batch_size : int
        Batch size for data loading. Default: 32
    
    Returns:
    --------
    generator
        Test data generator
    """
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    test_path = os.path.join(data_dir, 'test')
    test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    
    return test_generator


if __name__ == "__main__":
    # Example usage
    data_directory = "../dataset/"
    
    # Get generators
    train_gen, val_gen = get_data_generators(data_directory)
    
    print("✓ Data generators created successfully!")
    print(f"Number of training batches: {train_gen.samples // train_gen.batch_size}")
    print(f"Number of validation batches: {val_gen.samples // val_gen.batch_size}")
    print(f"Number of classes: {train_gen.num_classes}")
    print(f"Class labels: {train_gen.class_indices}")
