import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from llm_runner import LLMRunner
from file_writer import write_to_file

class WebhookMessage(BaseModel):
    message: str

app = FastAPI()

@app.post("/message")
async def handle_message(incoming: WebhookMessage):
    print(incoming.message)
    ## run the llm execution in a standalone async task
    asyncio.create_task(LLMRunner().run_interaction(incoming.message, write_to_file))
    return {"status": "ok"}
