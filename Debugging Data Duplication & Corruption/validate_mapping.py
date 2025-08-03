import json
import csv

def validate_mapping(data, mapping):
    if not isinstance(mapping, dict):
        print("Mapping is invalid: Mapping must be a dictionary.")
        return False

    try:
        open_index = data[0].index(next(key for key, value in mapping.items() if value["mapping"] == "open"))
        low_index = data[0].index(next(key for key, value in mapping.items() if value["mapping"] == "low"))
        close_index = data[0].index(next(key for key, value in mapping.items() if value["mapping"] == "close"))
        high_index = data[0].index(next(key for key, value in mapping.items() if value["mapping"] == "high"))
        volume_index = data[0].index(next(key for key, value in mapping.items() if value["mapping"] == "volume"))
    except StopIteration:
        print("Mapping is invalid: One or more required mappings (open, low, close, high, volume) are missing.")
        return False
    except ValueError:
        print("Mapping is invalid: One or more mapped columns not found in data header.")
        return False

    for row in data[1:]:
        try:
            open_value = float(row[open_index])
            low = float(row[low_index])
            close = float(row[close_index])
            high = float(row[high_index])
            volume = float(row[volume_index])
        except ValueError:
            print("Data is invalid: Non-numeric data found in a mapped column.")
            return False

        if not (low <= close <= high):
            print(f"Data is invalid: low ({low}) <= close ({close}) <= high ({high}) condition is not met in row: {row}")
            return False

        if not (low <= open_value <= high):
            print(f"Data is invalid: low ({low}) <= open ({open_value}) <= high ({high}) condition is not met in row: {row}")
            return False

        if not (volume > 0):
            print(f"Data is invalid: volume ({volume}) must be positive in row: {row}")
            return False

        max_magnitude = max(abs(float(x)) for x in row)
        if abs(volume) != max_magnitude:
            print(f"Data is invalid: volume ({volume}) is not the largest magnitude in row: {row}")
            return False

    print("Mapping and data are valid")
    return True

if __name__ == "__main__":
    try:
        with open("./mapping.json", "r") as f:
            mapping = json.load(f)
    except FileNotFoundError:
        print("Mapping file not found.")
        exit()
    except json.JSONDecodeError:
        print("Mapping file is not a valid JSON.")
        exit()

    try:
        with open("./02_sample_data_with_fabricated_columns.csv", "r") as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError:
        print("Data file not found.")
        exit()

    validate_mapping(data, mapping)
