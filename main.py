from langchain_ollama import ChatOllama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = ChatOllama(
    model="qwen3:4b"
)


response = model.invoke("Hey there! How are you doing today?")




class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = model.invoke(request.message)
    return {
        "response": response.content
        }