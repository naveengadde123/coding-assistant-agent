# Basic Coding Assistant Agent 🤖

A specialized AI Agent that takes any coding problem description, produces optimized, clean solution code in your chosen programming language, and provides a clear breakdown of the logic, algorithmic approach, and time/space complexity.

---

## 🌟 Key Features

- **Multi-Language Generation**: Generates idiomatic solution code in Python, JavaScript, TypeScript, C++, Java, Go, Rust, C#, and more.
- **In-Depth Logic Explanation**: Breaks down the strategy, steps, data structures, and edge cases.
- **Complexity Analysis**: Delivers precise Big-O Time and Space complexity evaluations.
- **Flexible LLM Backends**:
  - **Google Gemini** (Recommended: official `google-genai` SDK, ultra-fast `gemini-2.5-flash` / `gemini-2.0-flash`).
  - **Groq** (LLaMA 3.3 70B, ultra-fast inference).
  - **OpenAI** (GPT-4o, GPT-4o-mini).
  - **Offline Mock Fallback** (Instant testing out of the box without any API keys).
- **Dual Interface**:
  - **CLI Mode**: Interactive terminal chat and single-command flags.
  - **Streamlit Web UI**: Interactive visual dashboard with quick example buttons and syntax highlighting.

---

## 📁 Project Structure

```
coding-assistant-agent/
├── agent.py            # Core Agent class (Prompt engineering, LLM orchestration)
├── main.py             # CLI application (Interactive & command-line arguments)
├── app.py              # Streamlit Web UI dashboard
├── requirements.txt    # Python dependencies (google-genai, streamlit, etc.)
├── .env                # Local environment variables (GEMINI_API_KEY)
├── .env.example        # Environment variable template
└── README.md           # Documentation
```

---

## 🚀 Quickstart Guide

### 1. Configure Gemini API Key

Open the [.env](file:///c:/AI-Projects/coding-assistant-agent/.env) file:
```ini
# Get a free Gemini API key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=AIzaSyYourKeyHere
DEFAULT_PROVIDER=gemini
```
```ini
# Free API key at https://console.groq.com/
GROQ_API_KEY=gsk_your_groq_api_key_here

# Or OpenAI
# OPENAI_API_KEY=sk-proj-your_openai_api_key_here
```

*(Note: If you run without keys, the agent will seamlessly run in **Offline Mock Mode** so you can test the UI/CLI immediately).*

---

## 💻 Running the Interfaces

### Option A: Interactive CLI

Run interactively:
```bash
python main.py
```

Or pass problem arguments directly:
```bash
python main.py --problem "Write a function to check if a binary tree is symmetric" --language python
```

### Option B: Streamlit Web UI

Start the web dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8502`.

---

## 🧪 Programmatic Python Usage

You can also import and use the agent directly inside your own Python projects:

```python
from agent import CodingAssistantAgent

# Initialize agent
agent = CodingAssistantAgent(provider="groq")  # or "openai", or "mock"

# Solve a problem
result = agent.solve(
    problem="Given a string, find the length of the longest substring without repeating characters.",
    language="python"
)

if result["success"]:
    print(result["response"])
else:
    print("Error:", result["error"])
```