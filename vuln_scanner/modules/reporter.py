import json

def save_json_report(data, filename="scan_report.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)