# Parallel and Distributed Computing Lab (SP22-BCS-113)

This repository contains the lab examination project for the **Parallel and Distributed Computing** course. It compares the performance of a task (image processing) using three different execution models:

1.  **Sequential:** `sequential_process.py` - A single-threaded baseline implementation.
2.  **Parallel (Multiprocessing):** `parallel_process.py` - Uses Python's `multiprocessing` library to split the work across multiple CPU cores on a single machine.
3.  **Distributed (Simulation):** `distributed_sim.py` - Simulates the task being split and processed by two separate nodes.

---

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPOSITORY_URL]
    cd [YOUR_REPOSITORY_NAME]
    ```
2.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    *(You may need to create a `requirements.txt` file if you use libraries like `Pillow`, `numpy`, etc.)*
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute the scripts:**
    ```bash
    # Run the sequential version
    python sequential_process.py

    # Run the parallel version (will test 1, 2, 4, and 8 workers)
    python parallel_process.py

    # Run the distributed simulation
    python distributed_sim.py
    ```

---

## 📊 Performance Results & Analysis

Here is a summary of the findings from `report.txt`.

### Task 1: Sequential Time

* **Sequential Processing Time:** 1.25 seconds (for a "cold" run)

### Task 2: Parallel Speedup (Multiprocessing)

This table shows the performance when using Python's `multiprocessing` library on a single machine. The "1 Worker" time of 0.46s is used as the baseline (a "warm" run).

| Workers | Time (s) | Speedup |
| :---: | :---: | :---: |
| 1 | 0.46 | 1.00x |
| 2 | 0.74 | 0.62x |
| 4 | 0.44 | 1.05x |
| 8 | 0.39 | 1.18x |

### Task 3: Distributed Simulation

This simulation split the workload between two "nodes."

* **Node 1:** Processed 47 images in 0.2s
* **Node 2:** Processed 47 images in 0.2s
* **Total Distributed Time:** 0.4s
* **Calculated Efficiency:** 41.17x (over sequential)

### Key Analysis

The results are... interesting.

* **Best Parallel Performance:** 8 workers gave the fastest time (0.39s), but the speedup was minimal (1.18x).
* **The 2-Worker Problem:** Performance was **worse** (0.74s) than the 1-worker baseline (0.46s). This indicates the *overhead* of creating and managing the worker processes was greater than any time saved by splitting the work.
* **Primary Bottleneck:** The task itself is already very fast (0.46s on a warm run). The fixed cost of spinning up Python's `multiprocessing` pool is a significant portion of that time. This is a classic **overhead-bound problem**. The minimal gains show that for *this specific fast task*, parallelization adds more cost than benefit.