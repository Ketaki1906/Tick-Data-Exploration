import pandas as pd
from datetime import datetime
import random
from collections import defaultdict
import argparse

def parse_ts(ts: str) -> datetime:
    """
    Parse an ISO8601 timestamp with optional fractional seconds ending in Z
    into a timezone-aware datetime.
    """
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)

def main(input_path):
    df = pd.read_csv(input_path)
    df['timestamp'] = df['timestamp'].apply(parse_ts)

    df['ts_binned'] = df['timestamp'].dt.round('5ms')

    grp = df.groupby(['symbol', 'ts_binned'])

    dup_stats = grp['price'].agg(
        occurrences='size',
        min_price='min',
        max_price='max'
    ).reset_index()

    dup_stats['price_shift'] = dup_stats['max_price'] - dup_stats['min_price']
    duplication_analysis = dup_stats[dup_stats['occurrences'] > 1].copy()
    duplication_analysis = duplication_analysis.rename(columns={'ts_binned': 'timestamp'})
    duplication_analysis = duplication_analysis[[
        'symbol',
        'timestamp',
        'occurrences',
        'price_shift'
    ]]
    duplication_analysis['timestamp'] = duplication_analysis['timestamp'].apply(lambda dt: dt.isoformat().replace('+00:00', 'Z'))
    duplication_analysis.to_csv('duplication_analysis.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and deduplicate timestamped data.")
    parser.add_argument('--input_path', type=str, required=True, help='Path to the input CSV file')

    args = parser.parse_args()

    input_path = args.input_path
    main(input_path)
