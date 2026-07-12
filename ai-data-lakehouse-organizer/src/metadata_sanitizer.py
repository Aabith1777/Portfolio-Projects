from pathlib import Path

from privacy.utils import load_json, save_json


METADATA_PATH = Path("outputs/metadata_report.json")
PRIVACY_PATH = Path("outputs/privacy_report.json")
OUTPUT_PATH = Path("outputs/safe_metadata.json")


class MetadataSanitizer:

    def __init__(self):

        self.metadata = []

        self.privacy = []

    # ----------------------------------------------------

    def load_files(self):

        self.metadata = load_json(
            METADATA_PATH
        )

        self.privacy = load_json(
            PRIVACY_PATH
        )

    # ----------------------------------------------------

    def build_lookup(self):

        lookup = {}

        for table in self.privacy["tables"]:

            table_lookup = {}

            for column in table["sensitive_columns"]:

                table_lookup[column["column"]] = column

            lookup[table["table_name"]] = table_lookup

        return lookup

    # ----------------------------------------------------

    def sanitize(self):

        lookup = self.build_lookup()

        safe_metadata = []

        for table in self.metadata:

            table_name = table["table_name"]

            safe_table = {

                "table_name": table_name,

                "file_name": table["file_name"],

                "row_count": table["row_count"],

                "column_count": table["column_count"],

                "columns": []

            }

            sensitive_lookup = lookup.get(

                table_name,

                {}

            )

            for column in table["columns"]:

                safe_column = column.copy()

                column_name = column["column_name"]

                if column_name in sensitive_lookup:

                    privacy = sensitive_lookup[

                        column_name

                    ]

                    action = privacy["action"]

                    if action == "MASK":
                        safe_column["column_name"] = (
                            f"<{privacy['classification']}>"
                        )

                    elif action == "REMOVE":
                        safe_column["column_name"] = (
                            f"<{privacy['classification']}>"
                        )

                    safe_column["classification"] = privacy[
                        "classification"
                    ]

                    safe_column["category"] = privacy[
                        "category"
                    ]

                    safe_column["severity"] = privacy[
                        "severity"
                    ]

                    safe_column["action"] = action

                else:

                    safe_column["classification"] = "BUSINESS_DATA"

                    safe_column["action"] = "NONE"

                safe_table["columns"].append(

                    safe_column

                )

            safe_metadata.append(

                safe_table

            )

        return safe_metadata

    # ----------------------------------------------------

    def run(self):

        print("\nLoading metadata...")

        self.load_files()

        print("Sanitizing metadata...")

        safe_metadata = self.sanitize()

        save_json(

            safe_metadata,

            OUTPUT_PATH

        )

        print("\nMetadata Sanitizer completed!")

        print(

            f"Output written to {OUTPUT_PATH}"

        )


def main():

    sanitizer = MetadataSanitizer()

    sanitizer.run()


if __name__ == "__main__":

    main()