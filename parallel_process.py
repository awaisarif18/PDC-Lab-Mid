# [File: parallel_process.py]
# 

import os
import time
from PIL import Image, ImageDraw, ImageFont
import multiprocessing  # The core library for this task
from concurrent.futures import ThreadPoolExecutor # The alternative 

# --- Configuration (Same as sequential) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(SCRIPT_DIR, 'images_dataset')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_parallel')      # Different output directory [cite: 32]
TARGET_SIZE = (128, 128)
WATERMARK_TEXT = "CUI-LHR SP23"

# --- Helper Function (The 'Task') ---
# This function must be at the top level (not inside another function)
# so that other processes can import and run it.
def process_image(image_paths):
    """
    Takes a tuple of (input_path, output_path) and processes the image.
    This is the "work" that each parallel worker will do.
    """
    input_path, output_path = image_paths # Unpack the tuple
    
    try:
        with Image.open(input_path) as img:
            img = img.resize(TARGET_SIZE, Image.LANCZOS)

            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 10)
            except IOError:
                font = ImageFont.load_default()

            text_position = (5, TARGET_SIZE[1] - 15)
            text_color = (255, 255, 255)
            draw.text(text_position, WATERMARK_TEXT, font=font, fill=text_color)

            # Create the output sub-directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path)
        
        # Return True on success
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        # Return False on failure
        return False

# --- Main Function ---
def main():
    print("Starting parallel processing...")
    
    # --- 1. Get the list of tasks (all images) ---
    # This part is still sequential, as we need the full list first.
    tasks = [] # This will be a list of (input_path, output_path) tuples
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, SOURCE_DIR)
                output_path = os.path.join(OUTPUT_DIR, relative_path)
                tasks.append((input_path, output_path))

    print(f"Found {len(tasks)} images to process.")
    
    # --- 2. Run Sequential (1 Worker) to get baseline ---
    # We can't import from sequential_process.py easily,
    # so we just run the 1-worker version here as our baseline.
    print("\nRunning with 1 worker (Baseline)...")
    start_seq = time.perf_counter()
    
    # map() applies the function to each item in the 'tasks' list
    # We use a list comprehension to force it to execute now.
    results_seq = [process_image(task) for task in tasks]
    
    end_seq = time.perf_counter()
    baseline_time = end_seq - start_seq
    print(f"1 Worker Time: {baseline_time:.2f} s")

    # --- 3. Define worker counts and run parallel tests ---
    # [cite: 32]
    worker_counts = [2, 4, 8] 
    
    # Get your machine's core count as a reference
    cpu_count = os.cpu_count()
    print(f"(Your system has {cpu_count} logical cores) [cite: 71]")
    
    results_table = []
    # Add baseline to our table [cite: 37, 38]
    results_table.append((1, baseline_time, 1.0))

    # --- Option A: Using multiprocessing.Pool (Recommended)  ---
    print("\n--- Testing with multiprocessing.Pool ---")
    for count in worker_counts:
        print(f"Running with {count} processes...")
        start_time = time.perf_counter()

        # Create a process pool with 'count' number of workers
        with multiprocessing.Pool(processes=count) as pool:
            # pool.map distributes the 'tasks' list among the workers
            #
            # It takes the 'process_image' function and one item from
            # the 'tasks' list at a time and gives it to a free worker.
            # It blocks until all tasks are complete.
            results = pool.map(process_image, tasks)

        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Calculate speedup
        speedup = baseline_time / total_time
        results_table.append((count, total_time, speedup))
        print(f"{count} Processes Time: {total_time:.2f} s (Speedup: {speedup:.2f}x)")

    # --- Option B: Using ThreadPoolExecutor (Alternative)  ---
    # Note: For this CPU-bound task, threads are slower than processes
    # due to Python's Global Interpreter Lock (GIL). But the exam
    # allows it, so you could use this code instead.
    
    # print("\n--- Testing with ThreadPoolExecutor ---")
    # for count in worker_counts:
    #     print(f"Running with {count} threads...")
    #     start_time = time.perf_counter()

    #     with ThreadPoolExecutor(max_workers=count) as executor:
    #         # executor.map works just like pool.map
    #         results = list(executor.map(process_image, tasks))

    #     end_time = time.perf_counter()
    #     total_time = end_time - start_time
        
    #     speedup = baseline_time / total_time
    #     # Add to table if not already there
    #     # results_table.append((count, total_time, speedup)) 
    #     print(f"{count} Threads Time: {total_time:.2f} s (Speedup: {speedup:.2f}x)")


    # --- 4. Display the speedup table ---
    # [cite: 34, 35]
    print("\n" + "="*30)
    print("      Speedup Table")
    print("="*30)
    print(f"{'Workers':<8} | {'Time (s)':<10} | {'Speedup':<8}") # [cite: 36]
    print("-" * 30)
    for workers, time_s, speedup in results_table:
        print(f"{workers:<8} | {time_s:<10.2f} | {speedup:<8.2f}x")
    print("="*30)


# This "if __name__ == '__main__':" block is ESSENTIAL for multiprocessing.
# It prevents child processes from re-running the main script when
# they are spawned. Without this, you get an infinite loop or errors.
if __name__ == "__main__":
    main()