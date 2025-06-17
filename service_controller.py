from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.domain.load import Load
from llm.load_mapper import map_load_to_products
from llm.llm_executor import LlmExecutor
import json
import os
from datetime import datetime
from model.domain.events.handler.load_products_handler import (
    LoadProductsHandler,
)
from model.domain.events.publish.load_products_publisher import (
    LoadProductsPublisher,
)

app = FastAPI()


@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})


@app.post("/load")
async def load_service(load: Load):
    messages = map_load_to_products(load)
    try:
        service_loaded = json.loads(
            LlmExecutor().run_completion(
                f"instagram:{load.instagram} messages: {messages}"
            )
        )
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
            )
        }
    )
