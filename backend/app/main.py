# backend/app/main.py
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our custom modules
from app.utils.pdf_parser import extract_text_from_pdf
from app.graph.workflow import app_graph

app = FastAPI(title="MockMate AI", version="1.0")

# CORS: Allow Frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- IN-MEMORY DATABASE (For simple state management) ---
# Format: { "session_id": { "resume_text": "...", "messages": [...] } }
SESSIONS = {}

# --- DATA MODELS ---
class ChatRequest(BaseModel):
    session_id: str
    answer: str

# --- ENDPOINTS ---

@app.get("/")
def health_check():
    return {"status": "running", "sessions_active": len(SESSIONS)}

@app.post("/start-interview")
async def start_interview(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    1. Reads the PDF.
    2. Initializes the Graph State.
    3. Generates the FIRST question.
    """
    # 1. Extract Text
    try:
        resume_text = await extract_text_from_pdf(resume)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid PDF: {str(e)}")

    # 2. Initialize State
    session_id = str(uuid.uuid4())
    initial_state = {
        "resume_text": resume_text,
        "job_description": job_description,
        "messages": [],      # Empty history
        "question_count": 0,
        "feedback": ""
    }

    # 3. Run Graph (Invokes 'ask_question' node)
    # The graph will see empty history and generate the first greeting/question.
    result = app_graph.invoke(initial_state)

    # 4. Save State & Return
    SESSIONS[session_id] = result
    
    # Get the AI's first message (the last message in the list)
    ai_message = result["messages"][-1]

    return {
        "session_id": session_id,
        "message": ai_message
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    1. Fetches session.
    2. Adds user's answer to history.
    3. Runs Graph to get NEXT question.
    """
    session_id = request.session_id
    
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")

    # 1. Retrieve current state
    current_state = SESSIONS[session_id]
    
    # 2. Append User's Answer to 'messages'
    # We add it manually because the API is the "Human Node"
    current_state["messages"].append(request.answer)

    # 3. Run Graph again
    # The graph will see the new user answer and generate the NEXT question
    new_result = app_graph.invoke(current_state)

    # 4. Update State
    SESSIONS[session_id] = new_result
    
    # 5. Extract AI Response
    ai_message = new_result["messages"][-1]

    # Check if interview is over (based on our logic in workflow.py)
    # Note: We need to handle the "End" logic in Frontend usually, 
    # but here we can just return the message.
    
    return {
        "message": ai_message,
        "question_count": new_result["question_count"]
    }