import json
import sys
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent

SRC_PATH = PROJECT_ROOT / "src"

RAW_DATA_PATH = PROJECT_ROOT / "sample_data" / "raw"

OUTPUTS_PATH = PROJECT_ROOT / "outputs"

METADATA_PATH = OUTPUTS_PATH / "metadata_report.json"
QUALITY_PATH = OUTPUTS_PATH / "data_quality_report.json"
RELATIONSHIPS_PATH = OUTPUTS_PATH / "relationships.json"
PRIVACY_PATH = OUTPUTS_PATH / "privacy_report.json"
SANITIZED_PATH = OUTPUTS_PATH / "sanitized_metadata.json"
AI_RECOMMENDATIONS_PATH = OUTPUTS_PATH / "ai_schema_recommendations.json"
LINEAGE_PATH = OUTPUTS_PATH / "lineage_report.json"
GLOSSARY_PATH = OUTPUTS_PATH / "business_glossary.json"

SQL_PATH = PROJECT_ROOT / "sql" / "silver"

sys.path.insert(0, str(SRC_PATH))

from pipeline import run_pipeline


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def load_json(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_uploaded_files(uploaded_files):

    RAW_DATA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    for file in RAW_DATA_PATH.glob("*.csv"):
        file.unlink()

    for uploaded_file in uploaded_files:

        output_file = RAW_DATA_PATH / uploaded_file.name

        with open(output_file, "wb") as file:

            file.write(uploaded_file.getbuffer())


def reports_exist():

    required = [

        METADATA_PATH,

        QUALITY_PATH,

        RELATIONSHIPS_PATH,

        PRIVACY_PATH,

        SANITIZED_PATH,

        AI_RECOMMENDATIONS_PATH,

        LINEAGE_PATH,

        GLOSSARY_PATH

    ]

    return all(path.exists() for path in required)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    st.set_page_config(

        page_title="AI Data Lakehouse Organizer",

        page_icon="🤖",

        layout="wide"

    )

    st.title("🤖 AI Data Lakehouse Organizer")

    st.caption(
        "Enterprise Metadata Intelligence Platform"
    )

    st.divider()

    st.header("Upload Dataset")

    uploaded_files = st.file_uploader(

        "Upload related CSV files",

        type=["csv"],

        accept_multiple_files=True

    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} file(s) selected."
        )

        for file in uploaded_files:

            st.write(f"• {file.name}")

    run_button = st.button(

        "Analyze & Organize",

        type="primary",

        disabled=not uploaded_files

    )

    if run_button:

        try:

            with st.spinner(
                "Running pipeline..."
            ):

                save_uploaded_files(uploaded_files)

                run_pipeline()

            st.success(
                "Pipeline completed successfully."
            )

            st.rerun()

        except Exception as error:

            st.exception(error)

            return

    st.divider()

    if not reports_exist():

        st.info(
            "Upload CSV files and run the pipeline."
        )

        return

    metadata = load_json(METADATA_PATH)

    quality = load_json(QUALITY_PATH)

    relationships = load_json(RELATIONSHIPS_PATH)

    privacy = load_json(PRIVACY_PATH)

    sanitized = load_json(SANITIZED_PATH)

    ai = load_json(AI_RECOMMENDATIONS_PATH)

    lineage = load_json(LINEAGE_PATH)

    glossary = load_json(GLOSSARY_PATH)

    sql_files = sorted(SQL_PATH.glob("*.sql"))

    total_tables = len(metadata)

    total_columns = sum(
        table["column_count"]
        for table in metadata
    )

    sensitive_columns = privacy["summary"][
        "sensitive_columns_detected"
    ]

    business_domains = lineage["summary"][
        "business_domains"
    ]

    total_relationships = len(relationships)

    total_sql = len(sql_files)

    tabs = st.tabs([

        "🏠 Overview",

        "📂 Metadata",

        "📊 Data Quality",

        "🔗 Relationships",

        "🔒 Privacy",

        "🧹 Sanitized Metadata",

        "🏗 AI Schema",

        "📝 Generated SQL",

        "📈 Lineage",

        "📖 Business Glossary"

    ])
        # =====================================================
    # OVERVIEW
    # =====================================================

    with tabs[0]:

        st.header("Project Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Tables", total_tables)
        col2.metric("Columns", total_columns)
        col3.metric("Relationships", total_relationships)

        col4, col5, col6 = st.columns(3)

        col4.metric("Sensitive Columns", sensitive_columns)
        col5.metric("Business Domains", business_domains)
        col6.metric("Generated SQL Files", total_sql)

        st.divider()

        st.subheader("Generated Reports")

        reports = [
            ("Metadata", METADATA_PATH),
            ("Data Quality", QUALITY_PATH),
            ("Relationships", RELATIONSHIPS_PATH),
            ("Privacy", PRIVACY_PATH),
            ("Sanitized Metadata", SANITIZED_PATH),
            ("AI Schema", AI_RECOMMENDATIONS_PATH),
            ("Lineage", LINEAGE_PATH),
            ("Business Glossary", GLOSSARY_PATH),
        ]

        for report_name, report_path in reports:

            if report_path.exists():
                st.success(f"✅ {report_name}")
            else:
                st.error(f"❌ {report_name}")

    # =====================================================
    # METADATA
    # =====================================================

    with tabs[1]:

        st.header("Metadata Report")

        for table in metadata:

            with st.expander(
                f"{table['table_name']} ({table['row_count']} rows)"
            ):

                st.write(
                    f"**Columns :** {table['column_count']}"
                )

                st.dataframe(
                    table["columns"],
                    use_container_width=True
                )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    with tabs[2]:

        st.header("Data Quality Report")

        if isinstance(quality, dict):

            if "summary" in quality:

                st.subheader("Summary")

                st.json(quality["summary"])

            if "tables" in quality:

                for table in quality["tables"]:

                    with st.expander(table["table_name"]):

                        st.json(table)

        else:

            st.json(quality)

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    with tabs[3]:

        st.header("Detected Relationships")

        if relationships:

            st.dataframe(
                relationships,
                use_container_width=True
            )

        else:

            st.info("No relationships detected.")

    # =====================================================
    # PRIVACY
    # =====================================================

    with tabs[4]:

        st.header("Privacy Report")

        st.subheader("Summary")

        st.json(
            privacy["summary"]
        )

        st.divider()

        for table in privacy["tables"]:

            with st.expander(table["table_name"]):

                if table["sensitive_columns"]:

                    st.subheader("Sensitive Columns")

                    st.dataframe(
                        table["sensitive_columns"],
                        use_container_width=True
                    )

                else:

                    st.success(
                        "No sensitive columns detected."
                    )

    # =====================================================
    # SANITIZED METADATA
    # =====================================================

    with tabs[5]:

        st.header("Sanitized Metadata")

        st.json(
            sanitized
        )
            # =====================================================
    # OVERVIEW
    # =====================================================

    with tabs[0]:

        st.header("Project Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Tables", total_tables)
        col2.metric("Columns", total_columns)
        col3.metric("Relationships", total_relationships)

        col4, col5, col6 = st.columns(3)

        col4.metric("Sensitive Columns", sensitive_columns)
        col5.metric("Business Domains", business_domains)
        col6.metric("Generated SQL Files", total_sql)

        st.divider()

        st.subheader("Generated Reports")

        reports = [
            ("Metadata", METADATA_PATH),
            ("Data Quality", QUALITY_PATH),
            ("Relationships", RELATIONSHIPS_PATH),
            ("Privacy", PRIVACY_PATH),
            ("Sanitized Metadata", SANITIZED_PATH),
            ("AI Schema", AI_RECOMMENDATIONS_PATH),
            ("Lineage", LINEAGE_PATH),
            ("Business Glossary", GLOSSARY_PATH),
        ]

        for report_name, report_path in reports:

            if report_path.exists():
                st.success(f"✅ {report_name}")
            else:
                st.error(f"❌ {report_name}")

    # =====================================================
    # METADATA
    # =====================================================

    with tabs[1]:

        st.header("Metadata Report")

        for table in metadata:

            with st.expander(
                f"{table['table_name']} ({table['row_count']} rows)"
            ):

                st.write(
                    f"**Columns :** {table['column_count']}"
                )

                st.dataframe(
                    table["columns"],
                    use_container_width=True
                )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    with tabs[2]:

        st.header("Data Quality Report")

        if isinstance(quality, dict):

            if "summary" in quality:

                st.subheader("Summary")

                st.json(quality["summary"])

            if "tables" in quality:

                for table in quality["tables"]:

                    with st.expander(table["table_name"]):

                        st.json(table)

        else:

            st.json(quality)

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    with tabs[3]:

        st.header("Detected Relationships")

        if relationships:

            st.dataframe(
                relationships,
                use_container_width=True
            )

        else:

            st.info("No relationships detected.")

    # =====================================================
    # PRIVACY
    # =====================================================

    with tabs[4]:

        st.header("Privacy Report")

        st.subheader("Summary")

        st.json(
            privacy["summary"]
        )

        st.divider()

        for table in privacy["tables"]:

            with st.expander(table["table_name"]):

                if table["sensitive_columns"]:

                    st.subheader("Sensitive Columns")

                    st.dataframe(
                        table["sensitive_columns"],
                        use_container_width=True
                    )

                else:

                    st.success(
                        "No sensitive columns detected."
                    )

    # =====================================================
    # SANITIZED METADATA
    # =====================================================

    with tabs[5]:

        st.header("Sanitized Metadata")

        st.json(
            sanitized
        )