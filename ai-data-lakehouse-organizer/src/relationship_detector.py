import json
from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("sample_data/raw")
OUTPUT_PATH = Path("outputs/relationships.json")
MIN_MATCH_PERCENTAGE = 70


def load_all_tables():
    """Load every CSV file into a dictionary."""

    tables = {}

    csv_files = list(RAW_DATA_PATH.glob("*.csv"))

    for csv_file in csv_files:
        table_name = csv_file.stem
        tables[table_name] = pd.read_csv(csv_file)

    return tables


def compare_columns(parent_series, child_series):
    """Compare two columns and calculate how well their values match."""

    parent_values = set(
        parent_series.dropna().astype(str).str.strip()
    )

    child_values = set(
        child_series.dropna().astype(str).str.strip()
    )

    if len(child_values) == 0:
        return None

    matched_values = child_values.intersection(parent_values)

    orphan_values = child_values.difference(parent_values)

    match_percentage = round(
        (len(matched_values) / len(child_values)) * 100,
        2
    )

    return {
        "match_percentage": match_percentage,
        "matched_value_count": len(matched_values),
        "orphan_value_count": len(orphan_values),
        "orphan_values": sorted(orphan_values)
    }


def is_parent_candidate(column_name, series):
    """Check whether a column is likely to be a parent key."""

    non_null_values = series.dropna()

    if len(non_null_values) == 0:
        return False

    # Numeric columns are usually measures, not relationship keys
    if pd.api.types.is_numeric_dtype(series):
        return False

    column_upper = column_name.upper()

    # Reference-like columns are usually child/foreign-key columns
    child_patterns = [
        "REF",
        "REFERENCE"
    ]

    if any(
        pattern in column_upper
        for pattern in child_patterns
    ):
        return False

    # Parent keys usually have identifier-like names
    parent_patterns = [
        "_ID",
        "_CODE",
        "_KEY",
        "_NO",
        "_NUMBER"
    ]

    looks_like_identifier = any(
        pattern in column_upper
        for pattern in parent_patterns
    )

    if not looks_like_identifier:
        return False

    # Calculate uniqueness
    uniqueness_ratio = (
        non_null_values.nunique()
        / len(non_null_values)
    )

    # Allow some duplicate values because real-world data may be dirty
    return uniqueness_ratio >= 0.80


def detect_relationships(tables):
    """Compare columns across different tables and find relationships."""

    relationships = []

    table_names = list(tables.keys())

    for parent_table_name in table_names:

        parent_df = tables[parent_table_name]

        for child_table_name in table_names:

            # Do not compare a table with itself
            if parent_table_name == child_table_name:
                continue

            child_df = tables[child_table_name]

            for parent_column in parent_df.columns:

                parent_series = parent_df[parent_column]

                # IMPORTANT:
                # Skip columns that cannot act as parent keys
                if not is_parent_candidate(
                    parent_column,
                    parent_series
                ):
                    continue

                for child_column in child_df.columns:

                    child_series = child_df[child_column]

                    result = compare_columns(
                        parent_series,
                        child_series
                    )

                    if result is None:
                        continue

                    if (
                        result["match_percentage"]
                        >= MIN_MATCH_PERCENTAGE
                    ):

                        relationship = {
                            "parent_table": parent_table_name,
                            "parent_column": parent_column,
                            "child_table": child_table_name,
                            "child_column": child_column,
                            **result
                        }

                        relationships.append(relationship)

    return relationships


def main():

    print("Loading all tables...")

    tables = load_all_tables()

    print(f"Tables loaded: {len(tables)}")

    print("\nDetecting relationships...")

    relationships = detect_relationships(tables)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_PATH, "w") as output_file:

        json.dump(
            relationships,
            output_file,
            indent=4
        )

    print("\nRelationship detection completed!")

    print(
        f"Relationships found: {len(relationships)}"
    )

    print(
        f"Report created at: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()