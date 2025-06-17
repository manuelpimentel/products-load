import time
import uuid


class LoadProductsEvent:
    def __init__(
        self,
        instagram: str,
        summary: str = None,
        service_id: str = None,
        timestamp: float = None,
        products: list[dict] = None,
    ):
        self.instagram = instagram
        self.summary = summary
        self.service_id = service_id if service_id is not None else str(uuid.uuid4())
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.products = products if products is not None else []

    def __repr__(self):
        return f"<LoadProductsEvent service_id={self.service_id} timestamp={self.timestamp}>"

    @staticmethod
    def build_event(instagram: str, summary: str, products: list[dict] = None):
        return LoadProductsEvent(
            instagram=instagram,
            summary=summary,
            products=products if products is not None else [],
            timestamp=time.time(),
        )
