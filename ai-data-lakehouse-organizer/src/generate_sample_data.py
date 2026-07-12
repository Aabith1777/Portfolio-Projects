import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("sample_data/raw")
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)


# 1. CUSTOMER DATA
customers = pd.DataFrame({
    "CUST_ID": ["C001", "C002", "C003", "C002", "C005", "C006"],
    "FULL_NM": [
        "Aamir Khan",
        "Priya S",
        "  Rahul Kumar  ",
        "Priya S",
        "Meena R",
        "JOHN DAVID"
    ],
    "EMAIL_ID": [
        "AAMIR@EMAIL.COM",
        None,
        "rahul@email.com",
        None,
        "meena@email.com",
        "john@email.com"
    ],
    "JOIN_DT": [
        "10-01-2025",
        "2025/02/15",
        "03-20-2025",
        "2025/02/15",
        "2025-04-25",
        "01/05/2025"
    ]
})


# 2. ORDER DATA
orders = pd.DataFrame({
    "ORD_ID": ["O1001", "O1002", "O1003", "O1004", "O1005", "O1006"],
    "CUST_REF": ["C001", "C002", "C003", "C005", "C999", "C006"],
    "ORD_DT": [
        "2025-05-01",
        "02/05/2025",
        "2025/05/03",
        "May 04 2025",
        "2025-05-05",
        None
    ],
    "ORDER_STATUS": [
        "Completed",
        "completed",
        "SHIPPED",
        "Cancelled",
        "INVALID_STATUS",
        "Pending"
    ],
    "TOTAL_AMT": ["1500.50", "2000", "999.99", "500", None, "1200"]
})


# 3. PRODUCT DATA
products = pd.DataFrame({
    "PROD_CODE": ["P101", "P102", "P103", "P104", "P105"],
    "PROD_NM": [
        "Laptop Stand",
        "Wireless Mouse",
        "  Mechanical Keyboard",
        "USB Cable  ",
        "Webcam"
    ],
    "CATEGORY": [
        "Accessories",
        "ACCESSORIES",
        "Computer",
        "accessories",
        None
    ],
    "PRICE": [1499.99, 799.50, 3499.00, 299.99, -500.00]
})


# 4. ORDER ITEM DATA
order_items = pd.DataFrame({
    "ITEM_ID": ["I001", "I002", "I003", "I004", "I005", "I006"],
    "ORDER_REF": ["O1001", "O1001", "O1002", "O1003", "O9999", "O1006"],
    "PRODUCT_REF": ["P101", "P102", "P103", "P101", "P105", "P999"],
    "QTY": [1, 2, 1, 0, 3, -1],
    "UNIT_PRICE": [1499.99, 799.50, 3499.00, 1499.99, None, 500.00]
})


# 5. PAYMENT DATA
payments = pd.DataFrame({
    "PAYMENT_ID": ["PAY001", "PAY002", "PAY003", "PAY004", "PAY004"],
    "ORDER_ID_REF": ["O1001", "O1002", "O1003", "O1004", "O1004"],
    "PAY_MODE": ["UPI", "Credit Card", "upi", None, None],
    "PAYMENT_AMT": [1500.50, 2000.00, 999.99, 500.00, 500.00],
    "PAYMENT_STATUS": ["SUCCESS", "Success", "FAILED", "Pending", "Pending"]
})


# 6. DELIVERY DATA
deliveries = pd.DataFrame({
    "TRACK_ID": ["T001", "T002", "T003", "T004", "T005"],
    "ORDER_REFERENCE": ["O1001", "O1002", "O1003", "O1005", "O8888"],
    "COURIER_NM": [
        "BlueDart",
        "DELHIVERY",
        "DTDC",
        None,
        "Unknown"
    ],
    "SHIP_DT": [
        "2025-05-02",
        "03/05/2025",
        "2025/05/04",
        None,
        "invalid_date"
    ],
    "DELIVERY_STATUS": [
        "Delivered",
        "IN TRANSIT",
        "delivered",
        "Pending",
        "LOST"
    ]
})


# Save all DataFrames as CSV files
datasets = {
    "cust_info_final.csv": customers,
    "order_dump_2025.csv": orders,
    "product_master_old.csv": products,
    "order_items_new.csv": order_items,
    "payment_txns_v2.csv": payments,
    "delivery_tracking.csv": deliveries
}


for file_name, dataframe in datasets.items():
    output_file = RAW_DATA_PATH / file_name
    dataframe.to_csv(output_file, index=False)
    print(f"Created: {file_name} ({len(dataframe)} rows)")


print("\nAll messy datasets created successfully!")