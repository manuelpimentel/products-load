from typing import Any
from model.domain.events.service_identified_event import ServiceIdentifiedEvent
import os
import json
from datetime import datetime


class ServiceIdentifiedHandler:

    def __init__(self, event: ServiceIdentifiedEvent) -> None:
        self.event = event

    def handle(self) -> None:
        """
        Handles the ServiceIdentified domain event.

        Args:
            event: The event instance containing relevant data.
        """

        print("Handling ServiceIdentified event")

        self.append_to_pending_file(
            date_str=datetime.fromtimestamp(self.event.timestamp).strftime("%d%m%y"),
            new_data={
                "instagram": self.event.instagram,
                "service_id": self.event.service_id,
                "timestamp": self.event.timestamp,
                "products": self.event.products,
            },
        )

        pass

    def append_to_pending_file(self, date_str: str, new_data: Any) -> None:
        """
        Appends new_data to input/pending/load_ddMMyy.json. If the file doesn't exist,
        it is created with the structure of input/load_120625.json.

        Args:
            date_str: Date string in ddMMyy format.
            new_data: Data to append (dict or list).
        """
        print(f"[DEBUG] append_to_pending_file called with date_str={date_str}")
        print(f"[DEBUG] new_data={new_data}")

        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../..")
        )
        pending_dir = os.path.join(project_root, "loads", "pending")

        filename = f"load_{date_str}.json"
        pending_file = os.path.join(pending_dir, filename)

        print(f"[DEBUG] pending_dir={pending_dir}")
        print(f"[DEBUG] pending_file={pending_file}")

        if not os.path.exists(pending_dir):
            print(f"[DEBUG] pending_dir does not exist, creating...")
            os.makedirs(pending_dir)

        if os.path.exists(pending_file):
            print(f"[DEBUG] pending_file exists, loading...")
            with open(pending_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            print(f"[DEBUG] pending_file does not exist, initializing empty list")
            data = []

        print(f"[DEBUG] data before append: {data}")

        if isinstance(new_data, list):
            data.extend(new_data)
        else:
            data.append(new_data)

        print(f"[DEBUG] data after append: {data}")

        try:
            with open(pending_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[DEBUG] Successfully wrote to {pending_file}")
        except Exception as e:
            print(f"[ERROR] Failed to write to {pending_file}: {e}")
