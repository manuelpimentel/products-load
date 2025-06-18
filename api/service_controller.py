import uuid
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.domain.load import Load
from llm.load_mapper import map_load_to_content
from llm.llm_executor import LlmExecutor
import json
from model.domain.events.publish.load_products_publisher import (
    LoadProductsPublisher,
)
from api.model.load_attempt import LoadAttempt

app = FastAPI()


@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})


@app.head("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})


@app.post("/load")
async def load_service(load: LoadAttempt):
    if not load.is_valid():
        print("Invalid load attempt:", load)
        return JSONResponse(
            content={
                "response": "Debes escribir el instagram del servicio. ejemplo: instagram: @viaia"
            },
            status_code=400,
        )
        
        
    content = map_load_to_content(load)

    try:
        service_loaded = json.loads(LlmExecutor().run_completion(content))
        service_loaded["id"] = str(uuid.uuid4())
        LoadProductsPublisher(service_loaded).publish()

    except Exception as e:
        print("Error during LLM execution:", e)
        return JSONResponse(
            content="No pude procesar la información, intenta de nuevo",
            status_code=500,
        )

    return JSONResponse(
        content={
            "response": service_loaded.get(
                "summary", "No pude generar un resumen, intenta de nuevo"
            ),
            "id": service_loaded.get("id", None),
        }
    )


@app.post("/validate")
def validate_load(load: Load):
    """
    Endpoint to validate the service load.
    """
    try:
        content = map_load_to_content(load)
        # Here you can add validation logic if needed
        return JSONResponse(
            content={"message": "Service load is valid", "content": content}
        )
    except Exception as e:
        logging.error(f"Validation error: {e}")
        return JSONResponse(
            content={"message": "Validation failed", "error": str(e)},
            status_code=400,
        )


logging.basicConfig(level=logging.INFO)  # Add this line to enable INFO logs to console
