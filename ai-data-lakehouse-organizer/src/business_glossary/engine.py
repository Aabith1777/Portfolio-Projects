# Business Glossary Engine
import os
import re
import time
from datetime import datetime, UTC
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

from .utils import load_json, save_json


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class PrivacySnapshot(BaseModel):
    """Privacy classification snapshot for a single column."""

    is_sensitive: bool
    classification: str | None = None
    category: str | None = None
    severity: str | None = None


class ColumnGlossary(BaseModel):
    """Business glossary entry for a single target column."""

    column: str
    business_description: str
    privacy: PrivacySnapshot


class TableGlossary(BaseModel):
    """Business glossary entry for a single target table."""

    business_domain: str
    table_name: str
    table_description: str
    columns: list[ColumnGlossary]


class GlossaryResponse(BaseModel):
    """Gemini response schema — one table at a time."""

    columns: list[ColumnGlossary]


class BusinessGlossary(BaseModel):
    """Top-level business glossary document."""

    metadata: dict
    tables: list[TableGlossary]


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are a Senior Enterprise Data Steward.
Generate business glossary entries suitable for an enterprise data catalog.

Audience: Business Analysts, Data Engineers, Data Scientists, Business Users.

Rules:
- Write concise, clear business descriptions (1-2 sentences each).
- Do not change table names or column names.
- Do not invent new columns.
- Do not invent technical implementation details.
- Use enterprise terminology.
- Return valid JSON only.
"""


class BusinessGlossaryEngine:
    """Generates an enterprise business glossary from the lineage report."""

    def __init__(self) -> None:
        self.lineage_path = Path("outputs/lineage_report.json")
        self.output_path = Path("outputs/business_glossary.json")

        self.lineage: dict = {}
        self._client: genai.Client | None = None

    # --------------------------------------------------

    def _validate_inputs(self) -> None:
        """Ensure the lineage report exists before processing."""
        if not self.lineage_path.exists():
            raise FileNotFoundError(
                f"Required input file not found: {self.lineage_path}\n"
                "Run lineage_generator.py first to produce the lineage report."
            )

    # --------------------------------------------------

    def _load_lineage(self) -> None:
        """Load and store the lineage report."""
        print("Loading lineage...")
        self.lineage = load_json(self.lineage_path)

    # --------------------------------------------------

    def _init_gemini(self) -> None:
        """Load .env and initialise the Gemini client."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY was not found in the .env file."
            )
        self._client = genai.Client(api_key=api_key)

    # --------------------------------------------------

    def _build_privacy_snapshot(self, col: dict) -> PrivacySnapshot:
        """Extract privacy information from a lineage column entry."""
        priv = col.get("privacy", {})
        if priv.get("is_sensitive"):
            return PrivacySnapshot(
                is_sensitive=True,
                classification=priv.get("classification"),
                category=priv.get("category"),
                severity=priv.get("severity"),
            )
        return PrivacySnapshot(is_sensitive=False)

    # --------------------------------------------------

    def _generate_prompt(self, table: dict) -> str:
        """
        Build a focused, per-table prompt for Gemini.

        Only the fields relevant for documentation are included —
        the full lineage payload is never sent.
        """
        table_name = table["target_table"]
        business_domain = table.get("business_domain", "Unknown")
        table_description = table.get("table_description", "")

        column_lines: list[str] = []
        for col in table["columns"]:
            target = col["target_column"]
            priv = col.get("privacy", {})
            if priv.get("is_sensitive"):
                severity = priv.get("severity", "SENSITIVE")
                category = priv.get("category", "")
                privacy_label = f"{severity} {category}".strip()
            else:
                privacy_label = "Not Sensitive"
            column_lines.append(f"  - {target} ({privacy_label})")

        columns_block = "\n".join(column_lines)

        return f"""\
{_SYSTEM_PROMPT}

Business Domain : {business_domain}
Table           : {table_name}
Description     : {table_description}

Columns:
{columns_block}

Return a JSON object with a single key "columns".
Each entry must have:
  - "column": the exact column name as listed above.
  - "business_description": a concise enterprise-grade description.
  - "privacy": an object with "is_sensitive" (bool) and, when true,
    "classification", "category", and "severity" matching the input.

Do not add, remove, or rename any column.
"""

    # --------------------------------------------------

    _RETRY_ATTEMPTS = 3
    _DEFAULT_RETRY_DELAY = 30  # seconds

    def _parse_retry_delay(self, error_message: str) -> int:
        """Extract retry delay in seconds from a 429 error message."""
        match = re.search(r"retry in (\d+)", error_message)
        if match:
            return int(match.group(1)) + 2  # small buffer
        return self._DEFAULT_RETRY_DELAY

    def _call_gemini(self, prompt: str) -> GlossaryResponse:
        """
        Send a single table prompt to Gemini and return a validated response.

        Retries up to _RETRY_ATTEMPTS times on 429 RESOURCE_EXHAUSTED,
        honouring the retry delay suggested by the API.
        Raises on non-retryable failures or exhausted retries.
        """
        last_exc: Exception | None = None

        for attempt in range(1, self._RETRY_ATTEMPTS + 1):
            try:
                response = self._client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": GlossaryResponse.model_json_schema(),
                    },
                )
                return GlossaryResponse.model_validate_json(response.text)

            except Exception as exc:  # noqa: BLE001
                error_str = str(exc)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    delay = self._parse_retry_delay(error_str)
                    print(
                        f"  [RATE LIMIT] Attempt {attempt}/{self._RETRY_ATTEMPTS} "
                        f"— waiting {delay}s before retry..."
                    )
                    time.sleep(delay)
                    last_exc = exc
                else:
                    raise  # non-retryable — propagate immediately

        assert last_exc is not None  # guaranteed: loop ran _RETRY_ATTEMPTS times
        raise last_exc

    # --------------------------------------------------

    def _generate_glossary(self) -> list[TableGlossary]:
        """
        Iterate over every table in the lineage report and call Gemini.

        If Gemini fails for one table the error is logged and processing
        continues with the remaining tables.
        """
        tables: list[TableGlossary] = []
        inter_table_delay = 12  # seconds — stay within free-tier RPM

        for idx, table in enumerate(self.lineage.get("tables", [])):
            table_name = table["target_table"]
            print(f"Generating glossary for {table_name}")

            if idx > 0:
                time.sleep(inter_table_delay)

            prompt = self._generate_prompt(table)

            try:
                response = self._call_gemini(prompt)
            except Exception as exc:  # noqa: BLE001
                print(f"  [WARNING] Gemini failed for {table_name}: {exc}")
                print(f"  Skipping {table_name} and continuing...")
                continue

            # Merge AI-generated descriptions with privacy info from lineage
            enriched_columns: list[ColumnGlossary] = []
            ai_col_map = {c.column: c for c in response.columns}

            for lineage_col in table["columns"]:
                col_name = lineage_col["target_column"]
                ai_entry = ai_col_map.get(col_name)

                business_description = (
                    ai_entry.business_description
                    if ai_entry
                    else f"Column {col_name} in {table_name}."
                )

                privacy_snapshot = self._build_privacy_snapshot(lineage_col)

                enriched_columns.append(
                    ColumnGlossary(
                        column=col_name,
                        business_description=business_description,
                        privacy=privacy_snapshot,
                    )
                )

            tables.append(
                TableGlossary(
                    business_domain=table.get("business_domain", "Unknown"),
                    table_name=table_name,
                    table_description=table.get("table_description", ""),
                    columns=enriched_columns,
                )
            )

        return tables

    # --------------------------------------------------

    def _build_metadata(self, table_count: int) -> dict:
        """Build the top-level metadata block for the glossary report."""
        return {
            "version": "1.0",
            "generated_at": (
                datetime.now(UTC).replace(microsecond=0).isoformat()
            ),
            "generator": "AI Data Lakehouse Organizer",
            "tables": table_count,
        }

    # --------------------------------------------------

    def _save_report(self, glossary: BusinessGlossary) -> None:
        """Serialise the glossary to the output file."""
        print("Saving business glossary...")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        save_json(glossary.model_dump(), self.output_path)

    # --------------------------------------------------

    def run(self) -> None:
        """Execute the Business Glossary Engine."""
        self._validate_inputs()
        self._load_lineage()
        self._init_gemini()

        tables = self._generate_glossary()
        metadata = self._build_metadata(len(tables))

        glossary = BusinessGlossary(metadata=metadata, tables=tables)
        self._save_report(glossary)

        print("\nBusiness glossary generated successfully.")
        print(f"Tables documented : {len(tables)}")
        print(f"Report created at : {self.output_path}")
