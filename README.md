# Tick Data Exploration

Tick-by-tick financial market data to analyze data quality and telemetry for a real-time trading system.

## Project Structure

- **Reverse-Engineering Dataset Columns/**: Reverse-engineer the actual meaning of each column in a dataset of time-series telemetry with misleading column names.
- **Debugging Data Duplication & Corruption/**: Analyzing and debugging a real-time stream processing system for a high-frequency trading platform where race conditions introduce silent duplicates in the output.

## Key Features

- **Column Meaning Discovery:** Tools and scripts to infer and document the true semantics of  misleading dataset columns.
- **Data Quality Assurance:** Detects and reports missing values, silent duplicates, and potential data corruption due to race conditions.
- **Anomaly & Trend Visualization:** Interactive plots to highlight data trends, anomalies, and system performance metrics.
- **Debugging Utilities:** Utilities for tracing, identifying, and resolving data duplication and corruption issues in streaming pipelines.

## Getting Started

1. Clone the repository.
2. Follow instructions in the individual folders for running specific analyses.