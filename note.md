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


-------System Prompt----------
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(
        content="You are a helpful Python teacher."
    ),
    HumanMessage(
        content="What is a Python list?"
    )
]


update api 
@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        SystemMessage( content="""
    You are a Python tutor.

    Rules:
    - Explain concepts simply.
    - Give small examples.
    - Avoid unnecessary complexity.
    - Ask a question at the end.
    """),
        HumanMessage(content=request.message)
]
    response = model.invoke(messages)
    return {
        "response": response.content
        }


------Prompt Templates-----------

from langchain_core.prompts import ChatPromptTemplate
@app.post("/chat")
async def chat(request: ChatRequest):
   
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Your are a {role}. Explain concepts simply, give small examples, avoid unnecessary complexity, and ask a question at the end."
        ),
        (
            "human",
            "{message}"
        )
    ])
    messages = prompt.invoke({
        "role": "software engineer",
        "message": request.message
    })
    response = model.invoke(messages)
    return {
        "response": response.content
        }




-------Structured Output----------

uv add pydantic

class TopicAnalysis(BaseModel):
    topic: str
    difficulty: str
    summary: str

model = ChatOllama(
    model="ornith"
)

structured_model = model.with_structured_output(TopicAnalysis)




@app.post("/structured_chat")
async def structured_chat(request: ChatRequest): 
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a {role}. Analyze the topic and provide a structured response with topic, difficulty, and summary."
        ),
        (
            "human",
            "{message}"
        )
    ])
    messages = prompt.invoke({
        "role": "software engineer",
        "message": request.message
    })
    response = structured_model.invoke(messages)
    return response


-----------------












-----------------












-----------------






-----------------
