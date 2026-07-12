import json

def load_json(path):
    print(f"\nLoading file: {path.resolve()}")

    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="utf-16") as file:
            content = file.read()

    print(f"First 100 characters:\n{repr(content[:100])}")

    return json.loads(content)


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)