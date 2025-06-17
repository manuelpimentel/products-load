from model.domain.events.products_load_requested_event import ProductsLoadRequestedEvent
from datetime import datetime
from model.domain.events.handler.load_procucts_file_system import to_pending_loads


class LoadProductsHandler:

    def __init__(self, event: ProductsLoadRequestedEvent) -> None:
        self.event = event

    def handle(self) -> None:
        """
        Handles the ServiceIdentified domain event.

        Args:
            event: The event instance containing relevant data.
        """

        print("Handling ServiceIdentified event")

        to_pending_loads(
            date_str=datetime.fromtimestamp(self.event.timestamp).strftime("%d%m%y"),
            new_data={
                "instagram": self.event.instagram,
                "service_id": self.event.service_id,
                "timestamp": self.event.timestamp,
                "products": self.event.products,
            },
        )

        pass
