Create project folder 

initilize the env 
uv venv --python 3.12

uv init

-----

packages need 

uv add langchain fastapi uvicorn
langchain-ollama ( for the ollama support )

--- AI provider ----
we are going to use ollama model 
ollama --version 
ollama pull qwen3:4b 
ollama run qwen3:4b



----- build your first llm invoke -----
from langchain_ollama import ChatOllama


model = ChatOllama(
    model="qwen3:4b"
)

response = model.invoke(
    "What is an AI agent?"
)

print(response.content)

AIMessage
├── content
├── metadata
└── response information


now conenct with FAST API 
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama


app = FastAPI()

model = ChatOllama(
    model="qwen3:4b"
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    response = model.invoke(request.message)

    return {
        "response": response.content
    }


run this with this command 
uv run uvicorn main:app --reload