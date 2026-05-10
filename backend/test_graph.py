# backend/test_graph.py
from app.graph.workflow import app_graph

# Mock Data (Fake Resume/JD)
initial_state = {
    "resume_text": "I am a Python Developer with experience in FastAPI and React.",
    "job_description": "Looking for a Senior Python Engineer.",
    "messages": [],
    "question_count": 0,
    "feedback": ""
}

print("Thinking...")
# Run the graph
result = app_graph.invoke(initial_state)

print("\n--- AI Interviewer Says ---")
print(result["messages"][-1])
print("---------------------------")