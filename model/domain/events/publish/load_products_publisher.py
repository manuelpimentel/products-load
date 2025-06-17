from model.domain.events.products_load_requested_event import ProductsLoadRequestedEvent
from model.domain.events.handler.load_products_handler import (
    LoadProductsHandler,
)
import logging

logger = logging.getLogger(__name__)


class LoadProductsPublisher:
    def __init__(self, service_loaded: dict = None):
        self.event = ProductsLoadRequestedEvent.build_event(
            instagram=service_loaded.get("instagram"),
            id=service_loaded.get("id"),
            summary=service_loaded.get("summary"),
            products=service_loaded.get("products"),
        )

    def publish(self):
        logger.info(f"Publishing LoadProducts event: {self.event.__repr__()}")

        LoadProductsHandler(self.event).handle()
        return self.event
