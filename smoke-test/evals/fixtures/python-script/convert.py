"""Convert CSV to JSON with optional column filtering."""

import csv
import json
import sys


def convert_csv_to_json(input_path, output_path, columns=None):
    """Read a CSV file and write it as JSON.

    Args:
        input_path: Path to the input CSV file.
        output_path: Path to the output JSON file.
        columns: Optional list of column names to include. If None, include all.
    """
    with open(input_path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            if columns:
                filtered = {key: row[key] for key in columns if key in row}
                rows.append(filtered)
            else:
                rows.append(dict(row))

    with open(output_path, 'w') as json_file:
        json.dump(rows, json_file, indent=2)

    print(f"Converted {len(rows)} rows to {output_path}")
    return rows


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python convert.py <input.csv> <output.json> [col1,col2,...]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    filter_columns = sys.argv[3].split(',') if len(sys.argv) > 3 else None

    convert_csv_to_json(input_file, output_file, filter_columns)
