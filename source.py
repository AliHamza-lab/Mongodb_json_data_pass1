import os
import json
import urllib.parse
from pymongo import MongoClient, errors
import sys

# MongoDB client setup
mongodb_conn = "your_mongodb_connection_string"  # Replace with your MongoDB connection string
client = MongoClient(mongodb_conn)
admin = client['admin']

try:
    rootAdminPasswd = os.environ.get('ROOTADMIN_PASSWORD')
    cyberarkdbPasswd = os.environ.get('CYBERARKDB_PASSWORD')
except:
    print("Two Passwords required for rootAdmin/cyberark")
    sys.exit(1)

# Function to read JSON file
def read_json_file(file_path):
    with open(file_path, "r") as f:
        d = json.load(f)
    return d

# Function to insert user into MongoDB
def insert_user_into_mongodb(role, json_data):
    try:
        j = admin.command({"createUser": "rootAdmin", "pwd": rootAdminPasswd, "customData": json_data, "roles": role})
        print(j)
    except errors.OperationFailure as e:
        print("ERROR IS ", e)

# Main function
def main(role):
    json_file_path = "source.json"  # Specify the path to your JSON file
    json_data = read_json_file(json_file_path)
    insert_user_into_mongodb(role, json_data)

if __name__ == "__main__":
    role = "CN=DBaaS_MongoDB_Entitlements,OU=ARS_Unix,OU=Access Management,OU=Security Groups,OU=BAND,DC=corp,DC=bankofamerica,DC=com"  # Specify the role parameter
    main(role)
