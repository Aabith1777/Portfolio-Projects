import re


# ----------------------------------------------------------
# Common enterprise abbreviations
# ----------------------------------------------------------

ABBREVIATIONS = {

    "NM": "NAME",
    "FNM": "FIRST NAME",
    "LNM": "LAST NAME",

    "ADDR": "ADDRESS",

    "DOB": "DATE OF BIRTH",

    "EMP": "EMPLOYEE",

    "DEPT": "DEPARTMENT",

    "TEL": "TELEPHONE",

    "MOB": "MOBILE",

    "ACC": "ACCOUNT",

    "ACCT": "ACCOUNT",

    "NUM": "NUMBER",

    "NO": "NUMBER",

    "REF": "REFERENCE",

    "AMT": "AMOUNT",

    "DT": "DATE",

    "DESC": "DESCRIPTION",

    "QTY": "QUANTITY",

    "CAT": "CATEGORY",

    "LOC": "LOCATION",

    "CUST": "CUSTOMER",

    "PROD": "PRODUCT",

    "ORD": "ORDER",

    "PAY": "PAYMENT",

    "TXN": "TRANSACTION"

}


# ----------------------------------------------------------
# Stop words
# ----------------------------------------------------------

STOP_WORDS = {

    "THE",

    "OF",

    "FOR",

    "TO",

    "AND"

}


# ----------------------------------------------------------
# Normalize column name
# ----------------------------------------------------------

def normalize_column_name(column_name):
    """
    Convert a database column into normalized text.

    Example

    FULL_NM

    ->

    FULL NAME
    """

    text = column_name.upper()

    text = re.sub(
        r"[_\-.]",
        " ",
        text
    )

    words = text.split()

    expanded = []

    for word in words:

        expanded.append(

            ABBREVIATIONS.get(

                word,

                word

            )

        )

    normalized = " ".join(expanded)

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    ).strip()

    return normalized


# ----------------------------------------------------------
# Tokenize
# ----------------------------------------------------------

def tokenize_column_name(column_name):
    """
    Convert column into normalized tokens.

    Example

    FULL_NM

    ->

    ["FULL","NAME"]
    """

    normalized = normalize_column_name(
        column_name
    )

    tokens = normalized.split()

    tokens = [

        token

        for token in tokens

        if token not in STOP_WORDS

    ]

    return tokens