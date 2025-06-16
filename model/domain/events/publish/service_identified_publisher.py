from model.domain.events.service_identified_event import ServiceIdentifiedEvent
from model.domain.events.handler.service_identified_handler import (
    ServiceIdentifiedHandler,
)


class ServiceIdentifiedPublisher:
    def __init__(self, service_loaded: dict = None):
        self.event = ServiceIdentifiedEvent.build_event(
            instagram=service_loaded.get("instagram", ""),
            summary=service_loaded.get("summary", ""),
            products=service_loaded.get("products", []),
        )

    def publish(self):
        print("Publishing ServiceIdentified event")
        ServiceIdentifiedHandler(self.event).handle()
        return self.event
