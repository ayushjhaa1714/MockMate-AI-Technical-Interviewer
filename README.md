#  MockMate - AI Technical Interviewer

**MockMate** is an intelligent, full-stack AI agent that conducts real-time technical interviews. Unlike standard chatbots, it uses a **cyclic graph architecture (LangGraph)** to maintain interview state, evaluate candidate answers, and dynamically adjust difficulty based on the user's resume and job description.

🚀 **Live Demo:** [https://mock-mate-ten-sigma.vercel.app/](https://mock-mate-ten-sigma.vercel.app/)

---

## ✨ Key Features

-   **📄 Resume & JD Parsing:** Extracts skills from PDF resumes and aligns questions with the specific Job Description.
-   **🧠 Agentic Workflow (LangGraph):** Implements a stateful "Loop" (Ask → Wait → Evaluate → Decide). It remembers context and doesn't just hallucinate random questions.
-   **⚡ Real-Time Latency:** Powered by **Groq API (Llama 3)** for near-instant AI responses.
-   **🎨 Modern UI:** Clean, split-screen interface built with **React + Tailwind CSS**.
-   **🔒 PDF Security:** Parses resumes in-memory without storing sensitive data permanently.

---

## 🛠️ Tech Stack

### **Frontend**
* **Framework:** React (Vite)
* **Styling:** Tailwind CSS
* **State Management:** React Hooks
* **HTTP Client:** Axios
* **Deployment:** Vercel

### **Backend**
* **Framework:** FastAPI (Python)
* **AI Orchestration:** LangChain & LangGraph
* **LLM Provider:** Groq (Llama-3-8b)
* **PDF Processing:** PyPDF
* **Deployment:** Render
