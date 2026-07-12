import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


SAFE_METADATA_PATH = Path("outputs/safe_metadata.json")
QUALITY_PATH = Path("outputs/data_quality_report.json")
RELATIONSHIPS_PATH = Path("outputs/relationships.json")
OUTPUT_PATH = Path("outputs/ai_schema_recommendations.json")


class TableRecommendation(BaseModel):
    current_table_name: str
    business_domain: str
    recommended_table_name: str
    table_description: str
    recommended_columns: dict[str, str]


class SchemaRecommendations(BaseModel):
    tables: list[TableRecommendation]


def load_json(file_path: Path):
    """Load JSON file."""

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_input_files():
    """Ensure all required input files exist."""

    required_files = [
        SAFE_METADATA_PATH,
        QUALITY_PATH,
        RELATIONSHIPS_PATH
    ]

    missing = []

    for file in required_files:
        if not file.exists():
            missing.append(str(file))

    if missing:
        raise FileNotFoundError(
            "The following required files are missing:\n"
            + "\n".join(missing)
        )


def main():

    print("\nLoading AI Schema Analyzer...")

    validate_input_files()

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    print(f"API Key starts with: {api_key[:10]}...")
    print(f"API Key ends with: {api_key[-6:]}")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found in the .env file."
        )

    client = genai.Client(api_key=api_key)

    safe_metadata = load_json(SAFE_METADATA_PATH)
    quality_report = load_json(QUALITY_PATH)
    relationships = load_json(RELATIONSHIPS_PATH)

    prompt = f"""
You are an expert Cloud Data Architect specializing in designing enterprise
Data Lakehouse solutions.

The metadata below has ALREADY passed through a Privacy Guard.

Important:

- Sensitive column names have been masked.
- Personally identifiable information (PII) has already been protected.
- Never attempt to guess or reconstruct masked column names.
- Preserve masked columns exactly as provided.
- Recommend better names only for BUSINESS_DATA columns.

You are provided with:

1. Sanitized metadata
2. Data quality report
3. Relationship analysis

==================================================
SANITIZED METADATA
==================================================

{json.dumps(safe_metadata, indent=2)}

==================================================
DATA QUALITY REPORT
==================================================

{json.dumps(quality_report, indent=2)}

==================================================
RELATIONSHIPS
==================================================

{json.dumps(relationships, indent=2)}

For EVERY table:

1. Identify its business domain.

2. Recommend a clean snake_case table name.

3. Write a concise table description.

4. Recommend business-friendly snake_case names
   for BUSINESS_DATA columns.

5. Keep masked columns unchanged.

Rules:

- Do not remove any table.
- Do not remove any column.
- Do not rename masked columns.
- Preserve business meaning.
- Use analytics-friendly naming conventions.
- Return recommendations for every table.
"""

    print("\nSending sanitized metadata to Gemini...")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema":
                SchemaRecommendations.model_json_schema()
        }
    )

    recommendations = SchemaRecommendations.model_validate_json(
        response.text
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as output_file:

        json.dump(
            recommendations.model_dump(),
            output_file,
            indent=4
        )

    print("\nAI Schema Analysis Completed!")

    print(
        f"Tables analyzed : {len(recommendations.tables)}"
    )

    print(
        f"Output written to : {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()