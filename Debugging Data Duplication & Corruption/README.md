# Assesment 01: The Great Data Shuffle

## Installation Instructions

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Assumptions
- The data filed named `02_sample_data_with_fabricated_columns.csv` is present in this directory
- We are assuming that price is the last bidding done on the stock market for a particular stock. This supports our observation that the values of the `pulse` column can lie outside of the low-high range.'
- We are assuming that the data given is a time-series data for one stock.
- It was observed by us that the values of the stocks do become negative sometimes. We decided to overlook this observation.

## File Descriptions

- `analysis.ipynb`: Jupyter Notebook containing the data analysis for the assessment.
- `mapping.json`: JSON file containing the mapping between the original data and the fabricated columns.
- `requirements.txt`: Text file listing the Python dependencies for the project.
- `tnought_process.md`: Markdown file containing the thought process behind the analysis.
- `validate_mapping.py`: Python script that validates the mapping defined in `mapping.json`. To run the code, enter: `python3 validate_mapping.py`
