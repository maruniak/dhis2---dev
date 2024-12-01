import requests

# DHIS2 instance details
dhis2_url = "http://localhost:20511/api/metadata"  # Replace with your instance URL
username = "admin"
password = "district"

# File path to the JSON data
json_file_path = "configuration/csv/organisation_units.json"

# Read the JSON file
with open(json_file_path, "r", encoding="utf-8") as json_file:
    json_data = json_file.read()

# Make the POST request
response = requests.post(
    dhis2_url,
    auth=(username, password),
    headers={"Content-Type": "application/json"},
    data=json_data,
)

# Check the response
if response.status_code == 200:
    print("Metadata imported successfully!")
else:
    print(f"Failed to import metadata. Status code: {response.status_code}")
    print(f"Response: {response.text}")
