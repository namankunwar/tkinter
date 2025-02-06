import cv2
import numpy as np
import os

# Function to load images and convert to HSV
def load_and_convert_images(image_folder):
    hsv_values = []
    
    # Loop over images in the folder
    for image_name in os.listdir(image_folder):
        if image_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_folder, image_name)
            image = cv2.imread(image_path)
            
            # Convert the image to HSV
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Sample HSV values from the image (you could modify this to sample more points)
            sampled_hsv_values = hsv_image.reshape(-1, 3)  # Reshape to a 2D array of HSV values
            hsv_values.extend(sampled_hsv_values)  # Add the HSV values to the list

    return np.array(hsv_values)

# Function to calculate the optimal HSV range using percentiles
def calculate_percentile_hsv_range(hsv_values, lower_percentile=10, upper_percentile=90):
    # Separate out H, S, and V channels
    hue = hsv_values[:, 0]
    saturation = hsv_values[:, 1]
    value = hsv_values[:, 2]
    
    # Use percentiles, but ignore extreme low values for S and V (we can exclude 0 for S and V)
    lower_bound_hue = np.percentile(hue, lower_percentile)
    upper_bound_hue = np.percentile(hue, upper_percentile)
    
    lower_bound_saturation = np.percentile(saturation[saturation > 0], lower_percentile)  # Exclude 0 for S
    upper_bound_saturation = np.percentile(saturation[saturation > 0], upper_percentile)
    
    lower_bound_value = np.percentile(value[value > 0], lower_percentile)  # Exclude 0 for V
    upper_bound_value = np.percentile(value[value > 0], upper_percentile)
    
    # Combine the results for H, S, V
    lower_bound = [lower_bound_hue, lower_bound_saturation, lower_bound_value]
    upper_bound = [upper_bound_hue, upper_bound_saturation, upper_bound_value]
    
    return np.array(lower_bound), np.array(upper_bound)

# Path to your folders containing images for each category
image_folders = {
    'Undercooked': 'under_cooked',
    'Cooked': 'good',
    'Overcooked': 'over_cooked'
}

# Dictionary to store the HSV ranges for each category
hsv_ranges = {}

# Loop over each folder (category) and calculate the optimal HSV range
for category, folder_path in image_folders.items():
    # Load and analyze the images for each category
    hsv_values = load_and_convert_images(folder_path)
    
    # Calculate the optimal HSV range for the current category using the percentile method
    lower_bound, upper_bound = calculate_percentile_hsv_range(hsv_values)
    
    # Store the HSV ranges for each category
    hsv_ranges[category] = {'Lower Bound': lower_bound, 'Upper Bound': upper_bound}

# Print the optimal HSV ranges for each category
for category, bounds in hsv_ranges.items():
    print(f"\nOptimal HSV Range for {category}:")
    print(f"Lower Bound: {bounds['Lower Bound']}")
    print(f"Upper Bound: {bounds['Upper Bound']}")
