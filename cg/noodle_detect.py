import cv2
import numpy as np
import os

# Directly use the provided optimal HSV ranges
hsv_ranges = {
    "Undercooked": (np.array([2.22789693, 19.01544669, 26.5933439]), np.array([27.54907295, 125.61599479, 164.90275177])),  # Optimal range for Undercooked
    "Cooked": (np.array([3.79666201, 42.52226311, 73.98866768]), np.array([37.66618054, 156.32016564, 206.98224633])),        # Optimal range for Cooked
    "Overcooked": (np.array([0.0, 45.8441117, 22.43909766]), np.array([28.18915732, 191.13288994, 130.84372067]))  # Optimal range for Overcooked
}

# Function to get the HSV values from an image
def get_hsv_from_image(image_path):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv_image

# Function to check if a pixel is within the HSV range
def check_pixel_in_range(pixel, lower_bound, upper_bound):
    return np.all(pixel >= lower_bound) and np.all(pixel <= upper_bound)

# Function to process images and check if they fall within the defined HSV range
def process_images_for_range(folder_path, category):
    lower_bound, upper_bound = hsv_ranges[category]
    
    images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if file_path.endswith(('.jpg', '.png', '.jpeg')):
            hsv_image = get_hsv_from_image(file_path)
            
            # Iterate through each pixel and check if it is within the HSV range
            matching_pixels = 0
            total_pixels = hsv_image.shape[0] * hsv_image.shape[1]
            
            for row in hsv_image:
                for pixel in row:
                    if check_pixel_in_range(pixel, lower_bound, upper_bound):
                        matching_pixels += 1

            percentage_in_range = (matching_pixels / total_pixels) * 100
            images.append((filename, percentage_in_range))
    
    return images

# Define folder paths
undercooked_folder = 'under_cooked'
cooked_folder = 'good'
overcooked_folder = 'over'

# Process images and check if they fall within the range
undercooked_images = process_images_for_range(undercooked_folder, "Undercooked")
cooked_images = process_images_for_range(cooked_folder, "Cooked")
overcooked_images = process_images_for_range(overcooked_folder, "Overcooked")

# Print the results
print("\nUndercooked Images Analysis:")
for image, percentage in undercooked_images:
    print(f"{image}: {percentage:.2f}% of pixels in range")

print("\nCooked Images Analysis:")
for image, percentage in cooked_images:
    print(f"{image}: {percentage:.2f}% of pixels in range")

print("\nOvercooked Images Analysis:")
for image, percentage in overcooked_images:
    print(f"{image}: {percentage:.2f}% of pixels in range")
