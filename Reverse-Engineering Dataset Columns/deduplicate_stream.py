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

def main(input_path, output_path):
    df = pd.read_csv(input_path)
    df['timestamp'] = df['timestamp'].apply(parse_ts)

    real = []
    duplicate = []
    symbol_count = defaultdict(int)
    for _, row in df.iterrows():
        ts = row['timestamp']
        if ts.microsecond % 5000 == 0:
            symbol_count[row['symbol']] += 1
            real.append(row)
        else:
            duplicate.append(row)

    real_df = pd.DataFrame(real)

    duplicate_ts_mask = real_df.duplicated(subset=['timestamp'], keep=False)
    rows_with_same_timestamp = real_df[duplicate_ts_mask]

    real_df = real_df[~duplicate_ts_mask]
    real = [row for _, row in real_df.iterrows()]

    used_timestamps = set()
    for _, row in rows_with_same_timestamp.iterrows():
        ts = row['timestamp']
        if ts in used_timestamps:
            continue
        same_ts_rows = rows_with_same_timestamp[rows_with_same_timestamp['timestamp'] == ts]
        if len(same_ts_rows['symbol'].unique()) == 1:
            chosen_price = random.choice(same_ts_rows['price'].tolist())
            row_copy = row.copy()
            row_copy['price'] = chosen_price
            real.append(row_copy)
        else:
            symbols = same_ts_rows['symbol'].unique()
            least_count_symbol = min(symbols, key=lambda s: symbol_count[s])
            chosen_rows = same_ts_rows[same_ts_rows['symbol'] == least_count_symbol]
            if len(chosen_rows) == 1:
                real.append(chosen_rows.iloc[0])
            else:
                chosen_price = random.choice(chosen_rows['price'].tolist())
                row_copy = chosen_rows.iloc[0].copy()
                row_copy['price'] = chosen_price
                real.append(row_copy)
            symbol_count[least_count_symbol] += 1
        used_timestamps.add(ts)

    df_final = pd.DataFrame(real)
    df_final = df_final.sort_values(by='timestamp').reset_index(drop=True)
    df_final['timestamp'] = df_final['timestamp'].apply(lambda dt: dt.isoformat().replace('+00:00', 'Z'))
    df_final.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and deduplicate timestamped data.")
    parser.add_argument('--input_path', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--output_path', type=str, required=True, help='Path to save the processed CSV file')

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    main(input_path, output_path)
