from langchain_ollama import ChatOllama
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()
class TopicAnalysis(BaseModel):
    topic: str
    difficulty: str
    summary: str

model = ChatOllama(
    model="ornith"
)

structured_model = model.with_structured_output(TopicAnalysis)

# response = model.invoke(messages)


class ChatRequest(BaseModel):
    message: str


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