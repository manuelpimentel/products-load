from typing import Any
import os
import json
import logging

logger = logging.getLogger(__name__)

# Validation: check if service with same instagram already exists
def get_instagram(entry):
    return entry.get("instagram") if isinstance(entry, dict) else None

def to_pending_loads(date_str: str, new_data: Any) -> None:
    """
    Appends new_data to loads/pending/load_ddMMyy.json. If the file doesn't exist,
    it is created.

    Args:
        date_str: Date string in ddMMyy format.
        new_data: Data to append (dict or list).
    """

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../..")
    )
    pending_dir = os.path.join(project_root, "loads", "pending")

    filename = f"load_{date_str}.json"
    pending_file = os.path.join(pending_dir, filename)

    if not os.path.exists(pending_dir):
        os.makedirs(pending_dir)
        logger.info(f"Created directory: {pending_dir}")

    if os.path.exists(pending_file):
        with open(pending_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    existing_instagrams = {get_instagram(entry) for entry in data if get_instagram(entry)}

    # Support both dict and list for new_data
    new_entries = new_data if isinstance(new_data, list) else [new_data]
    filtered_new_entries = [
        entry for entry in new_entries
        if get_instagram(entry) not in existing_instagrams
    ]

    if not filtered_new_entries:
        logger.info("No new entries to append (all instagram values already exist).")
        return

    data.extend(filtered_new_entries)

    try:
        with open(pending_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Appended data to {pending_file}")
    except Exception as e:
        logger.error(f"Failed to write to {pending_file}: {e}")
