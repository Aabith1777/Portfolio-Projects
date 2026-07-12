import json
from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("sample_data/raw")
OUTPUT_PATH = Path("outputs/data_quality_report.json")


def add_issue(issues, issue_type, column, severity, details):
    """Add one standardized issue to the report."""
    issues.append({
        "issue_type": issue_type,
        "column": column,
        "severity": severity,
        "details": details
    })


def analyze_data_quality(file_path):
    df = pd.read_csv(file_path)

    issues = []

    # 1. Check duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    if duplicate_rows > 0:
        add_issue(
            issues,
            "duplicate_rows",
            None,
            "critical",
            f"Found {duplicate_rows} duplicate row(s)"
        )

    # 2. Analyze every column
    for column in df.columns:
        series = df[column]

        # Check missing values
        null_count = int(series.isna().sum())

        if null_count > 0:
            null_percentage = round(
                (null_count / len(df)) * 100,
                2
            )

            add_issue(
                issues,
                "missing_values",
                column,
                "warning",
                f"{null_count} missing value(s) ({null_percentage}%)"
            )

        # Check likely primary-key columns
        column_upper = column.upper()

        is_likely_id = (
            column_upper.endswith("_ID")
            or column_upper.endswith("_CODE")
            or column_upper in ["CUST_ID", "ORD_ID", "ITEM_ID", "TRACK_ID"]
        )

        if is_likely_id:
            duplicate_count = int(series.duplicated().sum())

            if duplicate_count > 0:
                add_issue(
                    issues,
                    "duplicate_identifier",
                    column,
                    "critical",
                    f"Found {duplicate_count} duplicate identifier value(s)"
                )

        # Check invalid numeric values
        numeric_keywords = [
            "QTY",
            "QUANTITY",
            "PRICE",
            "AMT",
            "AMOUNT"
        ]

        is_numeric_business_column = any(
            keyword in column_upper
            for keyword in numeric_keywords
        )

        if is_numeric_business_column and pd.api.types.is_numeric_dtype(series):
            invalid_count = int((series <= 0).sum())

            if invalid_count > 0:
                add_issue(
                    issues,
                    "invalid_numeric_value",
                    column,
                    "warning",
                    f"Found {invalid_count} zero or negative value(s)"
                )

        # Check text quality
        if pd.api.types.is_string_dtype(series):
            non_null_values = series.dropna().astype(str)

            # Leading or trailing spaces
            whitespace_count = int(
                (non_null_values != non_null_values.str.strip()).sum()
            )

            if whitespace_count > 0:
                add_issue(
                    issues,
                    "whitespace_issue",
                    column,
                    "warning",
                    f"Found {whitespace_count} value(s) with leading or trailing spaces"
                )

            # Inconsistent text casing
            normalized_values = non_null_values.str.strip().str.lower()

            if (
                normalized_values.nunique()
                < non_null_values.str.strip().nunique()
            ):
                add_issue(
                    issues,
                    "inconsistent_casing",
                    column,
                    "warning",
                    "Found values that differ only by uppercase/lowercase formatting"
                )

        # Check date-like columns
        date_keywords = ["DATE", "_DT", "SHIP_DT"]

        is_date_column = any(
            keyword in column_upper
            for keyword in date_keywords
        )

        if is_date_column:
            non_null_values = series.dropna()

            parsed_dates = pd.to_datetime(
                non_null_values,
                errors="coerce",
                format="mixed"
            )

            invalid_date_count = int(parsed_dates.isna().sum())

            if invalid_date_count > 0:
                add_issue(
                    issues,
                    "invalid_date",
                    column,
                    "critical",
                    f"Found {invalid_date_count} invalid date value(s)"
                )

    # Create summary
    critical_count = sum(
        issue["severity"] == "critical"
        for issue in issues
    )

    warning_count = sum(
        issue["severity"] == "warning"
        for issue in issues
    )

    report = {
        "table_name": file_path.stem,
        "row_count": len(df),
        "summary": {
            "total_issues": len(issues),
            "critical_issues": critical_count,
            "warnings": warning_count
        },
        "issues": issues
    }

    return report


def main():
    csv_files = list(RAW_DATA_PATH.glob("*.csv"))

    all_reports = []

    for csv_file in csv_files:
        print(f"Analyzing: {csv_file.name}")
        report = analyze_data_quality(csv_file)
        all_reports.append(report)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w") as output_file:
        json.dump(all_reports, output_file, indent=4)

    total_issues = sum(
        report["summary"]["total_issues"]
        for report in all_reports
    )

    print("\nSmart data quality analysis completed!")
    print(f"Tables analyzed: {len(all_reports)}")
    print(f"Total issues found: {total_issues}")
    print(f"Report created at: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()