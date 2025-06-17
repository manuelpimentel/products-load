from model.domain.events.load_products_event import LoadProductsEvent
from model.domain.events.handler.load_products_handler import (
    LoadProductsHandler,
)


class LoadProductsPublisher:
    def __init__(self, service_loaded: dict = None):
        self.event = LoadProductsEvent.build_event(
            instagram=service_loaded.get("instagram", ""),
            summary=service_loaded.get("summary", ""),
            products=service_loaded.get("products", []),
        )

    def publish(self):
        print("Publishing ServiceIdentified event")
        LoadProductsHandler(self.event).handle()
        return self.event
