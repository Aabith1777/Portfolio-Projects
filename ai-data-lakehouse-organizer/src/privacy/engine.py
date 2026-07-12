from pathlib import Path

from .utils import load_json, save_json
from .normalizer import tokenize_column_name


class PrivacyEngine:

    def __init__(self):

        self.metadata_path = Path(
            "outputs/metadata_report.json"
        )

        self.engine_config_path = Path(
            "config/privacy_engine.json"
        )

        self.rules_directory = Path(
            "config/rules"
        )

        self.output_path = Path(
            "outputs/privacy_report.json"
        )

        self.metadata = []

        self.rules = []

        self.minimum_confidence = 0

        self.feature_weights = {}

    # --------------------------------------------------

    def load_metadata(self):
        """Load metadata report."""

        self.metadata = load_json(
            self.metadata_path
        )

    # --------------------------------------------------

    def load_rules(self):
        """
        Load engine configuration and all rule files.
        """

        engine_config = load_json(
            self.engine_config_path
        )

        self.minimum_confidence = (
            engine_config["minimum_confidence"]
        )

        self.feature_weights = (
            engine_config["feature_weights"]
        )

        self.rules = []

        rule_files = sorted(
            self.rules_directory.glob("*.json")
        )

        print(
            f"\nLoading {len(rule_files)} rule files..."
        )

        for rule_file in rule_files:

            rule_config = load_json(
                rule_file
            )

            self.rules.extend(
                rule_config["rules"]
            )

            print(
                f"Loaded {rule_file.name} "
                f"({len(rule_config['rules'])} rules)"
            )

        print(
            f"Total rules loaded: {len(self.rules)}"
        )

    # --------------------------------------------------

    def evaluate_rule(
        self,
        column_name,
        rule
    ):
        """
        Evaluate rule against normalized tokens.
        """

        score = 0

        reasons = []

        tokens = tokenize_column_name(
            column_name
        )

        # ------------------------
        # Positive
        # ------------------------

        positive_matches = []

        for keyword in rule["positive_keywords"]:

            keyword_tokens = tokenize_column_name(
                keyword
            )

            if all(
                token in tokens
                for token in keyword_tokens
            ):
                positive_matches.append(
                    keyword
                )

        if positive_matches:

            best = max(
                positive_matches,
                key=len
            )

            score += rule["weight"]

            reasons.append(
                f"Matched '{best}'"
            )

        # ------------------------
        # Negative
        # ------------------------

        negative_matches = []

        for keyword in rule["negative_keywords"]:

            keyword_tokens = tokenize_column_name(
                keyword
            )

            if all(
                token in tokens
                for token in keyword_tokens
            ):
                negative_matches.append(
                    keyword
                )

        if negative_matches:

            best = max(
                negative_matches,
                key=len
            )

            score -= rule["weight"]

            reasons.append(
                f"Excluded '{best}'"
            )

        return score, reasons

    # --------------------------------------------------

    def classify_column(
        self,
        column
    ):
        """
        Classify a column using metadata.
        """

        best_result = {

            "classification": "BUSINESS_DATA",

            "category": "Business",

            "severity": "LOW",

            "description": "Business data",

            "action": "NONE",

            "confidence": 0,

            "score": 0,

            "reasons": []

        }

        for rule in self.rules:

            score, reasons = self.evaluate_rule(

                column["column_name"],

                rule

            )

            # ---------------------------------------
            # Feature 1 - String datatype
            # ---------------------------------------

            if (

                "str"

                in column["data_type"].lower()

                or

                "object"

                in column["data_type"].lower()

            ):

                score += self.feature_weights[
                    "string_datatype"
                ]

                reasons.append(
                    "String datatype"
                )

            # ---------------------------------------
            # Feature 2 - High uniqueness
            # ---------------------------------------

            if (

                column["uniqueness_ratio"]

                >= 0.80

            ):

                score += self.feature_weights[
                    "high_uniqueness"
                ]

                reasons.append(
                    "High uniqueness ratio"
                )

            # ---------------------------------------
            # Feature 3 - High null percentage
            # ---------------------------------------

            if (

                column["null_percentage"]

                >= 80

            ):

                score += self.feature_weights[
                    "high_null_percentage"
                ]

                reasons.append(
                    "Very high null percentage"
                )

            confidence = max(

                0,

                min(score, 100)

            )

            if (

                confidence >= self.minimum_confidence

                and

                confidence > best_result["confidence"]

            ):

                best_result = {

                    "classification": rule[
                        "classification"
                    ],

                    "category": rule[
                        "category"
                    ],

                    "severity": rule[
                        "severity"
                    ],

                    "description": rule[
                        "description"
                    ],

                    "action": rule[
                        "action"
                    ],

                    "confidence": confidence,

                    "score": score,

                    "reasons": reasons

                }

        return best_result

    # --------------------------------------------------

    def analyze_table(
        self,
        table
    ):
        """
        Analyze one table.
        """

        sensitive_columns = []

        safe_columns = []

        for column in table["columns"]:

            result = self.classify_column(
                column
            )

            if (

                result["classification"]

                == "BUSINESS_DATA"

            ):

                safe_columns.append({

                    "column": column[
                        "column_name"
                    ]

                })

            else:

                sensitive_columns.append({

                    "column": column[
                        "column_name"
                    ],

                    **result

                })

        return {

            "table_name": table[
                "table_name"
            ],

            "total_columns": len(
                table["columns"]
            ),

            "sensitive_column_count": len(
                sensitive_columns
            ),

            "safe_column_count": len(
                safe_columns
            ),

            "sensitive_columns": sensitive_columns,

            "safe_columns": safe_columns

        }

    # --------------------------------------------------

    def build_summary(
        self,
        report
    ):
        """
        Build summary.
        """

        severity_breakdown = {

            "LOW": 0,

            "MEDIUM": 0,

            "HIGH": 0,

            "CRITICAL": 0

        }

        total_sensitive = 0

        for table in report:

            total_sensitive += table[
                "sensitive_column_count"
            ]

            for column in table[
                "sensitive_columns"
            ]:

                severity = column["severity"]

                severity_breakdown[
                    severity
                ] += 1

        return {

            "tables_analyzed": len(
                report
            ),

            "sensitive_columns_detected": total_sensitive,

            "severity_breakdown": severity_breakdown

        }

    # --------------------------------------------------

    def run(self):
        """
        Execute Privacy Guard.
        """

        print(
            "\nLoading metadata..."
        )

        self.load_metadata()

        self.load_rules()

        report = []

        print(
            "\nAnalyzing tables..."
        )

        for table in self.metadata:

            report.append(

                self.analyze_table(
                    table
                )

            )

        final_report = {

            "summary": self.build_summary(
                report
            ),

            "tables": report

        }

        save_json(

            final_report,

            self.output_path

        )

        print(
            "\nPrivacy Guard completed!"
        )

        print(
            f"Tables analyzed: {len(report)}"
        )

        print(
            f"Sensitive columns detected: "
            f"{final_report['summary']['sensitive_columns_detected']}"
        )

        print(
            f"Report created at: {self.output_path}"
        )