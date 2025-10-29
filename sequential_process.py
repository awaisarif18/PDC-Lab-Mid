# [File: sequential_process.py]
# [cite: 22]

import os
import time
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(SCRIPT_DIR, 'images_dataset')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_seq')         # Folder for processed images [cite: 26]
TARGET_SIZE = (128, 128)            # Target resize dimensions 
WATERMARK_TEXT = "CUI-LHR SP23"     # Watermark text 

# --- Helper Function to Process a Single Image ---
def process_image(input_path, output_path):
    """
    Reads an image, resizes it, adds a watermark, and saves it.
    """
    try:
        # 1. Read the image [cite: 23]
        with Image.open(input_path) as img:
            # 2. Resize the image 
            img = img.resize(TARGET_SIZE, Image.LANCZOS)

            # 3. Add watermark 
            # Ensure image is in RGB mode to add a color watermark
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fall back to default if not found
            try:
                # You might need to change this path to a font file on your system
                font = ImageFont.truetype("arial.ttf", 10)
            except IOError:
                # print("Arial font not found, using default font.")
                font = ImageFont.load_default()

            # Position the text at the bottom-left
            text_position = (5, TARGET_SIZE[1] - 15) # 5px from left, 15px from bottom
            text_color = (255, 255, 255) # White
            
            draw.text(text_position, WATERMARK_TEXT, font=font, fill=text_color)

            # 4. Save the processed image
            # Ensure the output directory for this image's class exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path)
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

# --- Main Sequential Execution ---
def main():
    print("Starting sequential processing...")
    
    # Get the absolute start time
    total_start_time = time.perf_counter()

    image_files = []
    # os.walk() recursively finds all files in all subdirectories
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            # Simple check for common image file extensions
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                
                # Construct the full path to the source image
                input_path = os.path.join(root, file)
                
                # Construct the corresponding output path, preserving the subfolder structure
                # os.path.relpath gets the "relative" part (e.g., 'cats/cat1.jpg')
                relative_path = os.path.relpath(input_path, SOURCE_DIR)
                output_path = os.path.join(OUTPUT_DIR, relative_path)
                
                image_files.append((input_path, output_path))

    print(f"Found {len(image_files)} images to process.")

    # Loop through all found image paths and process them one by one
    for input_path, output_path in image_files:
        process_image(input_path, output_path)

    # Get the absolute end time and print the total
    total_end_time = time.perf_counter()
    
    print("-" * 30)
    # [cite: 28] (example format)
    print(f"Sequential Processing Time: {total_end_time - total_start_time:.2f} seconds")
    print(f"Processed images saved to '{OUTPUT_DIR}'")
    
    # Return the time so the parallel script can use it
    return total_end_time - total_start_time

if __name__ == "__main__":
    main()