# Assessment 02: Race Condition Replay

This assessment focuses on analyzing and debugging a real-time stream processing system for a high-frequency trading platform where race conditions introduce silent duplicates in the output.

## Running the code

### Requirements

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

### 1. Reconstruct Event Timelines

The `timeline_visualization.ipynb` identifies the overlapping processing windows (i.e. race conditions), retried jobs and failed events. It visualises the timeline of the worker system with the help of a Gantt plot.

### 2. Detect and Quantify Duplicates

To run the script:

```bash
python3 duplication_analysis.py --input_path 04_final_output.csv
```

This will generate the `duplication_analysis.csv` file in the same directory.

### 3. Write a De-duplication Script

To run the script:

```bash
python3 deduplicate_stream.py --input_path 04_final_output.csv --output_path deduplicated_output.csv
```

This will generate the `deduplicated_output.csv` file in the same directory.

## Assumptions
- The data files, `03_worker_logs.csv` and `04_final_output.csv`, are present in the same directory as the code files.
- It was observed by us that some of the events that got `timeout` in `03_worker_logs.csv` are present in the `04_final_output.csv`. This was counter-intuitive to us. Though, we could not solve it due to the input constraints posed by the question. To solve the same would be relatively trivial once multi-input files are allowed.

## File Descriptions

*   `duplication_analysis.csv`: Summary of duplication detection.
*   `duplication_analysis.py`: Python script used to generate the above mentioned Summary.
*   `deduplicate_stream.py`: Python script to de-duplicate the final output.
*   `timeline_visualization.ipynb`: Jupyter notebook that reconstructs event timelines.
*   `Report.md`: A report summarizing the findings and approach.
*   `future_improvements.md`: Suggestions for prevention strategies and future work.