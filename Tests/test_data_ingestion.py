import json
import csv
from pathlib import Path


def test_json_file_readable_and_not_empty():
    """Ensure the provided JSON file can be read and contains at least one record."""
    repo_root = Path(__file__).resolve().parents[1]
    json_path = repo_root / "Data" / "CapstoneJsonFile.json"

    assert json_path.exists(), f"Test data file not found: {json_path}"

    with json_path.open("r", encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except Exception as e:
            raise AssertionError(f"Failed to parse JSON file: {e}")

    # Accept either a list of records or a dict (object). Ensure there's content.
    if isinstance(data, list):
        assert len(data) > 0, "JSON file contains an empty list"
    elif isinstance(data, dict):
        assert len(data.keys()) > 0, "JSON file contains an empty object"
    else:
        # For other JSON root types (e.g. string/number), consider this a failure for our data expectations
        raise AssertionError(f"Unexpected JSON top-level type: {type(data)}")
    
def test_csv_file_readable_and_not_empty():
    """Ensure the provided CSV file can be read and contains at least one record."""
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "Data" / "Current_Employee_Names__Salaries__and_Position_Titles.csv"

    assert csv_path.exists(), f"Test data file not found: {csv_path}"

    with csv_path.open("r", encoding="utf-8", newline='') as fh:
        try:
            reader = csv.DictReader(fh)
            # Read one row to ensure there is data (skip header-only files)
            first_row = next(reader, None)
        except Exception as e:
            raise AssertionError(f"Failed to parse CSV file: {e}")

    assert first_row is not None, "CSV file contains no data rows"