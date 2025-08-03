# Report: Race Condition Replay

Analyzing a real-time stream processing system for a high-frequency trading platform where race conditions, retries are introducing duplicates in the output.

## Task 1: Reconstruct Event Timelines

1. Identify overlapping processing windows, retries and failed events in `03_worker_logs.csv`.
2. Create a timeline of which worker processed which event and when. 

### **Overlapping Processing Windows**:

We detect and group overlapping time intervals (start–end windows) within the same event, irrespective which worker did it.

#### Thought-Process

For each event, if the end time of that event is ahead of the start time of the same event which occurred any time in future, then we say that the processing windows have overlapped, regardless of the worker handling them. Thus, we say race condition has occurred here. With this logic, the function `assign_overlap_groups` helps to deduce the overlapping events and groups them together.

#### Explanation for the Output obtained

We observe that there are 250 unique overlapping processing windows for an event between same or different workers. For example, one of the overlapped events as detected by our algorithm is as follows:

```
| event_id    | worker_id | start_time                | end_time                  |
|-------------|-----------|---------------------------|---------------------------|
| evt_0001162 | worker-3  | 2025-07-12 09:15:05.810   | 2025-07-12 09:15:05.821   |
| evt_0001162 | worker-2  | 2025-07-12 09:15:05.810   | 2025-07-12 09:15:05.817   |
```

As, we can see here, the same event corresponding to event id `evt_0001162` overlaps. `evt_0001162` starts by worker-3 at `09:15:05.810`, and then is also started by worker-2 at `09:15:05.810`, before it ended by worker-3 at `09:15:05.821`. This is an overlapping event.

### **Retried Jobs**:

We identify the retried jobs as non-overlapping attempts to process the same event multiple times, possibly by the same or different workers.

#### Thought-Process

Here, when we encounter a new processing attempt for the same event_id starting after the previous attempt has ended ( i.e. non-overlapping) are identified as retries, irrespective of which worker handles it.

#### Explanation for the Output obtained

We observe that there are 0 retried jobs detected by our strategy in the given worker logs. This implies all the duplicates in the worker logs with respect to the event ids, are because of the overlapping processing windows (race conditions).

### **Failed events**:

We identify the failed jobs as the ones which did not get completed or crashed

#### Thought-Process

Here, whenever the status of a occurrence is not equal to `success`, we call it a failed job. As we can see that there only two unique values for status - `success` and  `timeout`. Further, we note that the occurrences having status `timeout`, have the value in the `end_time` column empty, indicating that the job did not complete and failed due to some reason.

#### Explanation for the Output obtained

We observe that there are 100 failed jobs detected by our strategy in the given worker logs. 

### **Gantt chart per worker**:

We plot the Gantt chart to analyse the distribution and timing of event processing across multiple workers.

Note: We plot only for the first 20 events occuring in `03_worker_logs.csv` for better readability.

#### Thought-Process

To observe the timeline and visualise it, we choose gantt chart as it enables us to see how tasks are handled concurrently by different workers and identify processing windows that overlap or retries if any.

#### Explanation for the Output obtained

We can make the following observations through the timeline depicted by the Gantt chart

1. Worker Distribution: Worker-1 seems to handle a large number of stocks. Worker-2 and Worker-3 show fewer or more spaced-out tasks This points to imbalanced load distribution between workers.

2. Many events seem to cluster around certain time windows (e.g., 09:15:00.15), which may indicate a burst of stock updates. This can be explained in Indian context as market open at 9:15 AM IST. 

3. Several events on the same or different workers start before the previous one has finished indicated by some blocks that overlap horizontally. As, we calculated there are 250 race conditions where the same stock is being accessed by different/same worker at the same time. We also see instances, like `evt_0000015` and `evt_0000016` in the Gantt plot where different events are accessed by the same person at overlapping time intervals, which can be considered as valid parallelism. 

4. Noticeable time gaps for some workers between events suggest that it is an idle time or delays that are occurring.

## Task 2: Detect and Quantify Duplicates

To detect and quantify duplicates, we used the `duplication_analysis.py` script. This script analyzes the input CSV file and identifies duplicate events based on the `symbol` and `timestamp` (rounded to `5ms`) columns.

#### Thought-Process

The `duplication_analysis.py` script groups the data by `symbol` and `ts_binned` (timestamp rounded to `5ms`), and then calculates the number of occurrences for each group. Duplicates are identified as groups with more than one occurrence. The script then saves the results to `duplication_analysis.csv`.

The reason for choosing `5ms` as the rounding value, was the following:

It was observed that the ticker for the data was a regular interval of `5ms`. Thus, to maintain consistency, and to remove obvious outliers, this was employed.

#### Explanation for the Output obtained

The `duplication_analysis.py` script generates a CSV file named `duplication_analysis.csv` containing the following columns: `symbol`, `timestamp (ts_binned)`, `occurrences`, and `price_shift`. The `occurrences` column indicates the number of times a particular `symbol` and `timestamp (ts_binned)` combination appears in the input data. The `price_shift` column indicates the difference between the maximum and minimum price for that combination.

To run the script, use the following command:

```bash
python3 duplication_analysis.py --input_path 04_final_output.csv
```

This will generate the `duplication_analysis.csv` file.

## Task 3: Write a De-duplication script

To de-duplicate the data, we used the `deduplicate_stream.py` script. This script reads the input CSV file, filters the data, removes duplicates, and saves the de-duplicated data to a new CSV file. (Both the CSV files are given as inputs through the CLI).

#### Thought Process

1. **Initial Filtering**  
   - **Rationale:** In our market data, true tick events always occur on 5 ms boundaries.  
   - **Action:** Keep only rows whose timestamp’s microsecond component is divisible by 5,000 μs (i.e. 5 ms); treat all others as anomalies.

2. **Identifying Duplicate Timestamps**  
   - Within the filtered set, find any timestamps that appear more than once.

3. **Resolving Exact Symbol+Timestamp Duplicates**  
   - **Case:** Same symbol **and** same timestamp, but different prices.  
   - **Strategy:** Choose one of the reported prices at random (no additional signal is available as the question states that only the `04_final_output.csv` file can be taken as input), and assign that as the “true” price.

4. **Resolving Timestamp‑Only Duplicates**  
   - **Case:** Same timestamp across different symbols.  
   - **Strategy:**  
     1. Select the symbol with the **lowest** occurrence count so far (to preserve the overall symbol distribution).  
     2. If multiple rows remain for that symbol, pick one price at random.  
   - **Result:** Guarantees exactly one event per timestamp, while respecting observed symbol frequencies (from the original ground truth data).

5. **Output**  
   - Combine the unique‐timestamp rows with the resolved duplicates.  
   - Sort by timestamp and write to the specified output CSV.

This pipeline ensures that each 5 ms boundary yields exactly one tick event, mitigating anomalies and race‑conditions without introducing external data.  

#### Explanation for the Output obtained

The `deduplicate_stream.py` script generates a CSV file containing the de-duplicated data. The script takes two arguments: the path to the input CSV file and the path to the output CSV file.

To run the script, use the following command:

```bash
python deduplicate_stream.py --input_path 04_final_output.csv --output_path deduplicated_output.csv
```

This will generate the `deduplicated_output.csv` file containing the de-duplicated data.

## **Root Cause Analysis**

### **Root Cause 1: Lack of Stream Ordering for Event Processing**

* **Problem:**
  Multiple workers are processing the same event (`event_id`)
simultaneously, often before the previous worker has completed the
task which is leading to overlapping start–end times. This may lead to
one update overwrite another and uncertainty of final state of event.

* **Cause:**
  The system does not enforce ordering or coordination across workers
per event. Thus, workers start processing, regardless of whether
someone else is already working on it.

### **Root Cause 2: Incomplete or Inaccurate Failure Handling**

* **Problem:**
  * The system lacks a mechanism for safe retry after timeout or error
which increases the likelihood of overlapping jobs.
* **Cause:**
  Jobs with a `timeout` status and no `end_time` were identified as
failed, but the system doesn’t appear to explicitely prevent future
attempts from starting on the same event while the previous one is
still active.

### **Root Cause 3: Insufficient Tick De-duplication Strategy**

* **Problem:**
  In the market data tick stream, multiple updates for the same
symbol-timestamp were found, where some were with different prices.

* **Cause:**
  Without explicit de-duplication logic based on `symbol` and
`timestamp`, inconsistent or duplicate ticks are stored, leading to
price jittering and wrong market interpretation. There is no check
like 1 update per symbol per 5ms tick etc.