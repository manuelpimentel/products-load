import json
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# --- CONFIGURATION ---
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = "Services"


def main(json_path):
    # Load JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    services = db[COLLECTION_NAME]

    for service in data:
        instagram = service.get("instagram")
        products = service.get("products")
        pending_to_persist = service.get("pending_to_persist")
        if not instagram:
            print("Skipping service without instagram.")
            continue

        update = {"products": products, "pending_to_persist": pending_to_persist}

        result = services.update_one({"instagram": instagram}, {"$set": update})

        if result.matched_count == 0:
            print(f"No service found for instagram: {instagram}")
        else:
            print(f"Updated service for instagram: {instagram}")

    client.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/update_services_with_products.py <json-file>")
        sys.exit(1)
    main(sys.argv[1])
