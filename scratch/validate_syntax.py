import json
import os

def validate_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[OK] {os.path.basename(file_path)} is valid JSON! Contains {len(data)} entries.")
        return True
    except Exception as e:
        print(f"[ERROR] Error parsing {os.path.basename(file_path)}: {str(e)}")
        return False

base_dir = os.path.dirname(__file__)
categories_path = os.path.join(base_dir, "../data/categories.json")
prompts_path = os.path.join(base_dir, "../data/prompts.json")

cat_valid = validate_json(categories_path)
prompts_valid = validate_json(prompts_path)

if cat_valid and prompts_valid:
    print("All data files validated successfully!")
    exit(0)
else:
    print("Data validation failed!")
    exit(1)
