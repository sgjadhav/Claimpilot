from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

# --- NEW: Import our LangGraph agent! ---
from agent import agent_executor 
from extractor import analyze_document

app = FastAPI(
    title="Claimpilot API",
    description="Backend API for Claimpilot",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Service is running"}

@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_extension = file.filename.split('.')[-1] if file.filename else ''
    result = analyze_document(file_bytes, file_extension)
    return {"extracted_text": result}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Format the user's message
        inputs = {"messages": [("user", request.message)]}
        
        # 2. NEW: Give this conversation a specific ID so the AI remembers it
        config = {"configurable": {"thread_id": "demo_web_session_1"}}
        
        # 3. Wake up the Agent, pass the message AND the memory config
        result = agent_executor.invoke(inputs, config=config)
        
        # 4. NEW: Safely extract the final answer text (fixes the Pydantic crash)
        raw_content = result["messages"][-1].content
        if isinstance(raw_content, list):
            # If the AI returns a list, grab the text block inside it
            final_answer = raw_content[0].get("text", str(raw_content))
        else:
            # If it's already a normal string, just use it
            final_answer = raw_content
            
        return ChatResponse(
            response=final_answer,
            status="success"
        )
    except Exception as e:
        return ChatResponse(
            response=f"The AI Brain encountered an error: {str(e)}",
            status="error"
        )