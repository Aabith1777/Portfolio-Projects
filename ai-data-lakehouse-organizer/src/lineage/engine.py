# Lineage Engine
import datetime
from pathlib import Path

from .utils import load_json, save_json


class LineageEngine:

    def __init__(self):
        self.metadata_path = Path("outputs/metadata_report.json")
        self.ai_path = Path("outputs/ai_schema_recommendations.json")
        self.privacy_path = Path("outputs/privacy_report.json")
        self.output_path = Path("outputs/lineage_report.json")

        self.metadata = []
        self.ai_recommendations = []
        self.privacy_report = {}

    # --------------------------------------------------

    def _validate_inputs(self):
        """Ensure all required input files exist."""
        required = [self.metadata_path, self.ai_path, self.privacy_path]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise FileNotFoundError(
                f"Required lineage input files are missing:\n" + "\n".join(missing)
            )

    # --------------------------------------------------

    def _load_files(self):
        """Load and parse the required input files."""
        self._validate_inputs()

        print("Loading metadata...")
        self.metadata = load_json(self.metadata_path)

        print("Loading AI recommendations...")
        self.ai_recommendations = load_json(self.ai_path)

        print("Loading privacy report...")
        self.privacy_report = load_json(self.privacy_path)

    # --------------------------------------------------

    def _build_metadata_lookup(self) -> dict:
        """
        Build lookup map: (table_name, column_name) -> metadata_dict
        """
        lookup = {}
        for table in self.metadata:
            table_name = table["table_name"]
            for col in table["columns"]:
                col_name = col["column_name"]
                lookup[(table_name, col_name)] = {
                    "data_type": col["data_type"],
                    "row_count": col["row_count"],
                    "null_percentage": col["null_percentage"],
                    "uniqueness_ratio": col["uniqueness_ratio"],
                }
        return lookup

    # --------------------------------------------------

    def _build_privacy_lookup(self) -> dict:
        """
        Build lookup map: (table_name, column_name) -> privacy_dict
        """
        lookup = {}
        tables = self.privacy_report.get("tables", [])
        for table in tables:
            table_name = table["table_name"]
            for col in table.get("sensitive_columns", []):
                col_name = col["column"]
                lookup[(table_name, col_name)] = {
                    "classification": col["classification"],
                    "category": col["category"],
                    "severity": col["severity"],
                    "action": col["action"]
                }
        return lookup

    # --------------------------------------------------

    def _generate_lineage_id(self, counter: int) -> str:
        """Generate sequential lineage ID (e.g. LIN-000001)."""
        return f"LIN-{counter:06d}"

    # --------------------------------------------------

    def _build_quality_snapshot(self, meta_info: dict) -> dict:
        """Build data quality snapshot with row count, null rate and uniqueness."""
        return {
            "row_count": meta_info.get("row_count", 0),
            "null_percentage": meta_info.get("null_percentage", 0.0),
            "uniqueness_ratio": meta_info.get("uniqueness_ratio", 0.0)
        }

    # --------------------------------------------------

    def _build_privacy_snapshot(self, privacy_info: dict) -> dict:
        """Build privacy snapshot dictionary."""
        if privacy_info is None:
            return {
                "is_sensitive": False
            }
        return {
            "is_sensitive": True,
            "classification": privacy_info.get("classification"),
            "category": privacy_info.get("category"),
            "severity": privacy_info.get("severity"),
            "action": privacy_info.get("action")
        }

    # --------------------------------------------------

    def _build_transformation_metadata(self, source_column: str, target_column: str) -> dict:
        """Return a nested transformation object with type and category."""
        if source_column != target_column:
            return {
                "type": "RENAME",
                "category": "COLUMN_STANDARDIZATION"
            }
        return {
            "type": "DIRECT_COPY",
            "category": "PASS_THROUGH"
        }

    # --------------------------------------------------

    def _generate_table_lineage(self) -> list:
        """
        Generate list of enriched table lineages.
        """
        metadata_lookup = self._build_metadata_lookup()
        privacy_lookup = self._build_privacy_lookup()

        lineage_tables = []
        recommendations = {
            table["current_table_name"]: table
            for table in self.ai_recommendations.get("tables", [])
        }

        col_counter = 1

        for table in self.metadata:
            source_table = table["table_name"]
            if source_table not in recommendations:
                continue

            rec = recommendations[source_table]
            target_table = rec["recommended_table_name"]
            column_mapping = rec["recommended_columns"]

            table_lineage = {
                "business_domain": rec.get("business_domain", "Unknown"),
                "table_description": rec.get("table_description", ""),
                "source_layer": "Bronze",
                "target_layer": "Silver",
                "source_table": source_table,
                "target_table": target_table,
                "columns": []
            }

            for column in table["columns"]:
                source_column = column["column_name"]
                target_column = column_mapping.get(source_column, source_column)

                meta_key = (source_table, source_column)
                meta_info = metadata_lookup.get(meta_key, {})
                privacy_info = privacy_lookup.get(meta_key, None)

                lineage_id = self._generate_lineage_id(col_counter)
                col_counter += 1

                trans_meta = self._build_transformation_metadata(source_column, target_column)
                quality_snapshot = self._build_quality_snapshot(meta_info)
                privacy_snapshot = self._build_privacy_snapshot(privacy_info)

                column_lineage = {
                    "lineage_id": lineage_id,
                    "source_column": source_column,
                    "target_column": target_column,
                    "source_data_type": meta_info.get("data_type", "unknown"),
                    "quality": quality_snapshot,
                    "privacy": privacy_snapshot,
                    "transformation": trans_meta,
                    "mapping_confidence": 100
                }

                table_lineage["columns"].append(column_lineage)

            lineage_tables.append(table_lineage)

        return lineage_tables

    # --------------------------------------------------

    def _generate_summary(self, tables: list, generated_at: str) -> dict:
        """
        Calculate lineage summary metrics.
        source_tables and target_tables are counts — full names live inside tables[].
        """
        total_tables = len(tables)
        total_mappings = 0
        business_domains = set()
        sensitive_columns_count = 0
        renamed_count = 0
        direct_copy_count = 0

        for table in tables:
            domain = table.get("business_domain")
            if domain:
                business_domains.add(domain)

            for col in table["columns"]:
                total_mappings += 1

                privacy_snap = col.get("privacy", {})
                if privacy_snap.get("is_sensitive"):
                    sensitive_columns_count += 1

                trans_type = col.get("transformation", {}).get("type")
                if trans_type == "RENAME":
                    renamed_count += 1
                elif trans_type == "DIRECT_COPY":
                    direct_copy_count += 1

        return {
            "version": "2.1",
            "generated_at": generated_at,
            "tables": total_tables,
            "source_tables": total_tables,
            "target_tables": total_tables,
            "column_mappings": total_mappings,
            "business_domains": len(business_domains),
            "sensitive_columns": sensitive_columns_count,
            "renamed_columns": renamed_count,
            "direct_copy_columns": direct_copy_count
        }

    # --------------------------------------------------

    def _generate_report_metadata(self, generated_at: str) -> dict:
        """Build top-level report metadata block."""
        return {
            "version": "2.1",
            "generator": "AI Data Lakehouse Organizer",
            "generated_at": generated_at,
            "pipeline_stage": "Silver Layer Preparation",
            "source_system": "CSV",
            "target_platform": "Google BigQuery"
        }

    # --------------------------------------------------

    def _save_report(self, report: dict):
        """Save lineage report to output directory."""
        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        save_json(report, self.output_path)

    # --------------------------------------------------

    def run(self):
        """
        Execute Enriched Lineage Engine.
        """
        self._load_files()

        from datetime import datetime, UTC

        generated_at = (
            datetime.now(UTC)
            .replace(microsecond=0)
            .isoformat()
        )

        metadata = self._generate_report_metadata(generated_at)

        tables = self._generate_table_lineage()
        summary = self._generate_summary(tables, generated_at)

        report = {
            "metadata": metadata,
            "summary": summary,
            "tables": tables
        }

        self._save_report(report)

        print("\nLineage generation completed!")
        print(f"Tables processed : {summary['tables']}")
        print(f"Column mappings : {summary['column_mappings']}")
        print(f"Business domains : {summary['business_domains']}")
        print(f"Sensitive columns : {summary['sensitive_columns']}")
        print(f"Renamed columns : {summary['renamed_columns']}")
        print(f"Direct copy columns : {summary['direct_copy_columns']}")
        print(f"Report created at : {self.output_path}")