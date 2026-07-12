import json
from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("sample_data/raw")
OUTPUT_PATH = Path("outputs/metadata_report.json")


def get_column_metadata(series, total_rows):
    """
    Build metadata for one column.
    """

    non_null_values = series.dropna()

    unique_count = int(non_null_values.nunique())

    null_count = int(series.isna().sum())

    if total_rows == 0:
        null_percentage = 0
    else:
        null_percentage = round(
            (null_count / total_rows) * 100,
            2
        )

    if len(non_null_values) == 0:
        uniqueness_ratio = 0
    else:
        uniqueness_ratio = round(
            unique_count / len(non_null_values),
            2
        )

    return {
        "column_name": series.name,
        "data_type": str(series.dtype),

        "row_count": total_rows,

        "null_count": null_count,
        "null_percentage": null_percentage,

        "unique_count": unique_count,
        "uniqueness_ratio": uniqueness_ratio
    }


def scan_csv(file_path):
    """
    Scan one CSV file.
    """

    df = pd.read_csv(file_path)

    total_rows = len(df)

    metadata = {
        "table_name": file_path.stem,
        "file_name": file_path.name,
        "row_count": total_rows,
        "column_count": len(df.columns),
        "columns": []
    }

    for column in df.columns:

        metadata["columns"].append(
            get_column_metadata(
                df[column],
                total_rows
            )
        )

    return metadata


def main():

    csv_files = list(
        RAW_DATA_PATH.glob("*.csv")
    )

    all_metadata = []

    for csv_file in csv_files:

        print(
            f"Scanning: {csv_file.name}"
        )

        metadata = scan_csv(csv_file)

        all_metadata.append(metadata)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w"
    ) as output_file:

        json.dump(
            all_metadata,
            output_file,
            indent=4
        )

    print("\nMetadata scan completed!")

    print(
        f"Tables scanned: {len(all_metadata)}"
    )

    print(
        f"Report created at: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()