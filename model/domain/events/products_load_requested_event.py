import time
import uuid


class ProductsLoadRequestedEvent:
    def __init__(
        self,
        instagram: str,
        id: str = None,
        summary: str = None,
        service_id: str = None,
        timestamp: float = None,
        products: list[dict] = None,
    ):
        self.instagram = instagram
        print(f"Setting id: {id}")
        self.id = id if id is not None else str(uuid.uuid4())
        self.summary = summary
        self.service_id = service_id
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.products = products if products is not None else []

    def __repr__(self):
        return f"<ProductsLoadRequestedEvent id={self.id} service_id={self.service_id} timestamp={self.timestamp}>"

    @staticmethod
    def build_event(instagram: str, id: str, summary: str, products: list[dict] = None):
        return ProductsLoadRequestedEvent(
            instagram=instagram,
            id=id,
            summary=summary,
            products=products if products is not None else [],
            timestamp=time.time(),
        )
