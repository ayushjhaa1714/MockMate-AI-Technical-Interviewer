# backend/app/graph/workflow.py
import os
from typing import TypedDict, List, Annotated
from dotenv import load_dotenv

# LangChain / LangGraph Imports
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq

# 1. Load Environment Variables
load_dotenv()

# 2. Setup the LLM (The "Brain")
# We use Llama-3-8b because it's fast and smart enough for interviews
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.7
)

# 3. Define the State (The "Memory")
# This dictates what data is passed between nodes
class InterviewState(TypedDict):
    resume_text: str          # Context from PDF
    job_description: str      # Context from User
    messages: List[str]       # Chat history
    question_count: int       # Track how many questions asked
    feedback: str             # Store feedback for the final report

# 4. Define Nodes (The "Actions")

def generate_question(state: InterviewState):
    """Node 1: Generates the next technical question."""
    
    # Simple prompt engineering
    messages = [
        SystemMessage(content=f"""
            You are a strict technical interviewer. 
            User Resume: {state['resume_text']}
            Job Description: {state['job_description']}
            
            Your goal: Ask a conceptual technical question based on the resume skills that fit the job description.
            - Do NOT ask generic questions like "Tell me about yourself".
            - Ask ONE specific technical question.
            - Keep it short.
        """)
    ] + [HumanMessage(content=m) for m in state["messages"]]
    
    response = llm.invoke(messages)
    
    # Return updated state
    return {
        "messages": state["messages"] + [response.content],
        "question_count": state["question_count"] + 1
    }

def evaluate_answer(state: InterviewState):
    """Node 2: Evaluates the user's answer (Simulated for this step)."""
    
    # In a real app, we would check the user's last message here.
    # For now, we just pass through to the logic layer.
    return {} 

# 5. Define the Graph (The "Flow")
workflow = StateGraph(InterviewState)

# Add Nodes
workflow.add_node("ask_question", generate_question)
# Note: We don't need a separate node for 'user_input' in the graph definition 
# because the API will handle the pause. We just need to know where to resume.

# Set Entry Point
workflow.set_entry_point("ask_question")

# 6. Define Conditional Logic (The "Loop")
def check_progress(state):
    if state["question_count"] >= 5:
        return "end"
    return "continue"

# This logic is usually handled by the API calling specific nodes, 
# but for a pure graph flow, we define edges like this:
workflow.add_edge("ask_question", END) # Simple version for first test

# Compile the graph
app_graph = workflow.compile()