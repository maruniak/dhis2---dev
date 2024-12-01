import csv
import json
import random
import string

# File paths
input_csv = "configuration/csv/organisation_units.csv"
output_json = "configuration/csv/organisation_units.json"

# DHIS2 UID generation function with checksum
def generate_uid():
    uid = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    uid += calculate_checksum(uid)
    return uid

def calculate_checksum(uid):
    factors = [2, 1]
    sum = 0
    characters = string.ascii_uppercase + string.digits  # A-Z + 0-9
    for i, char in enumerate(reversed(uid)):
        factor = factors[i % 2]
        code_point = ord(char)
        if char.isalpha():
            code_point -= 55  # A=10, B=11, ..., Z=35
        else:
            code_point -= ord('0')  # 0=0, 1=1, ..., 9=9
        addend = factor * code_point
        sum += addend // 36 + addend % 36
    return characters[(36 - sum % 36) % 36]

# Parse CSV and convert to JSON
organisation_units = []
uids = {}  # Store generated UIDs for parent-child relationships

with open(input_csv, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Generate or retrieve UID
        unit_id = row["Organisation unit ID"].strip()
        if unit_id not in uids:
            uids[unit_id] = generate_uid()

        # Build organisation unit object
        unit = {
            "id": uids[unit_id],
            "name": row["Name"].strip(),
            "shortName": row["Name"].strip(),
            "openingDate": row["Opening Date"].strip(),
        }

        # Add parent UID if parent exists
        parent_id = row["Parent ID"].strip()
        if parent_id:
            if parent_id not in uids:
                uids[parent_id] = generate_uid()
            unit["parent"] = {"id": uids[parent_id]}

        organisation_units.append(unit)

# Create JSON structure
metadata = {"organisationUnits": organisation_units}

# Save to JSON file
with open(output_json, "w", encoding="utf-8") as jsonfile:
    json.dump(metadata, jsonfile, ensure_ascii=False, indent=4)

print(f"Organisation units exported to {output_json}")
