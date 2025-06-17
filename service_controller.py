from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.domain.request import Request
from llm.messages_mapper import map_request_to_messages
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
async def load_service(request: Request):
    messages = map_request_to_messages(request)
    try:
        service_loaded = json.loads(
            LlmExecutor().run_completion(
                f"instagram:{request.instagram} messages: {messages}"
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
