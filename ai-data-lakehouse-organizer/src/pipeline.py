from metadata_scanner import main as run_metadata_scanner
from data_quality_analyzer import main as run_data_quality_analyzer
from relationship_detector import main as run_relationship_detector
from privacy_guard import main as run_privacy_guard
from metadata_sanitizer import main as run_metadata_sanitizer
from ai_schema_analyzer import main as run_ai_schema_analyzer
from sql_generator import main as run_sql_generator
from lineage_generator import main as run_lineage_generator
from business_glossary_generator import (
    main as run_business_glossary_generator,
)


def run_pipeline():
    """Run the complete AI Data Lakehouse Organizer pipeline."""

    print("\n==============================================")
    print(" AI DATA LAKEHOUSE ORGANIZER ")
    print("==============================================")

    print("\n[1/9] Metadata Scanner")
    run_metadata_scanner()

    print("\n[2/9] Data Quality Analyzer")
    run_data_quality_analyzer()

    print("\n[3/9] Relationship Detector")
    run_relationship_detector()

    print("\n[4/9] Privacy Guard")
    run_privacy_guard()

    print("\n[5/9] Metadata Sanitizer")
    run_metadata_sanitizer()

    print("\n[6/9] AI Schema Analyzer")
    run_ai_schema_analyzer()

    print("\n[7/9] SQL Generator")
    run_sql_generator()

    print("\n[8/9] Lineage Generator")
    run_lineage_generator()

    print("\n[9/9] Business Glossary Generator")
    run_business_glossary_generator()

    print("\n==============================================")
    print(" PIPELINE COMPLETED SUCCESSFULLY ")
    print("==============================================")


if __name__ == "__main__":
    run_pipeline()