import cv2
import numpy as np
import os
import glob

# Define folders
folders = {
    "Cooked": "good",
    "Undercooked": "under_cooked",
    "Overcooked": "over_cooked"
}

# Define HSV ranges for different noodle types
hsv_ranges = {
    "Undercooked": (np.array([0., 40., 60.]), np.array([25., 160., 210.])),  # Adjusted range for Undercooked
    "Cooked": (np.array([0., 35., 90.]), np.array([20., 150., 230.])),       # Adjusted range for Cooked
    "Overcooked": (np.array([0., 110., 50.]), np.array([15., 180., 150.]))   # Adjusted range for Overcooked
}
# Function to classify an image
def classify_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image {image_path}")
        return None

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    pixel_counts = {
        label: cv2.countNonZero(cv2.inRange(hsv, lower, upper))
        for label, (lower, upper) in hsv_ranges.items()
    }

    return max(pixel_counts, key=pixel_counts.get)

# Function to classify images in a given folder
def classify_images(folder_name, correct_type):
    folder_path = folders.get(folder_name)
    if not folder_path or not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.png"))
    total_images = len(image_files)
    correct_count = 0
    misclassified_images = []

    for image_path in image_files:
        filename = os.path.basename(image_path)
        detected_type = classify_image(image_path)

        if detected_type == correct_type:
            correct_count += 1
        else:
            misclassified_images.append((filename, detected_type))

    # Print results
    print(f"\n===== {folder_name} Folder Results =====")
    print(f"Total images: {total_images}")
    print(f"Correctly classified as {correct_type}: {correct_count}")
    print(f"Misclassified images: {len(misclassified_images)}")

    if misclassified_images:
        print("\nMisclassified Images:")
        for img, detected in misclassified_images:
            print(f"- {img} classified as {detected}")

# Run classification for all three folders
for folder, correct_type in folders.items():
    classify_images(folder, folder)
