"""
Streamlit Web UI for the Basic Coding Assistant Agent
Run with: streamlit run app.py
"""

import streamlit as st
import os
from agent import CodingAssistantAgent

# Page configuration
st.set_page_config(
    page_title="Coding Assistant Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-live {
        background-color: #DCFCE7;
        color: #166534;
    }
    .badge-mock {
        background-color: #FEF3C7;
        color: #92400E;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Provider & Model Settings
st.sidebar.header("⚙️ Agent Settings")

provider_choice = st.sidebar.selectbox(
    "Select LLM Provider",
    options=["Google Gemini (Recommended)", "Groq", "OpenAI", "Offline Demo / Mock"],
    index=0
)

api_key = None
provider_slug = "gemini"
model_name = None

if "Gemini" in provider_choice:
    provider_slug = "gemini"
    default_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        value=default_key,
        type="password",
        help="Get your key from https://aistudio.google.com/app/apikey"
    )
    model_name = st.sidebar.selectbox(
        "Gemini Model",
        options=["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        index=0
    )
elif "Groq" in provider_choice:
    provider_slug = "groq"
    default_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        help="Get a free key from console.groq.com"
    )
    model_name = st.sidebar.selectbox(
        "Groq Model",
        options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )
elif "OpenAI" in provider_choice:
    provider_slug = "openai"
    default_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        value=default_key,
        type="password",
        help="OpenAI API key from platform.openai.com"
    )
    model_name = st.sidebar.selectbox(
        "OpenAI Model",
        options=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )
else:
    provider_slug = "mock"
    st.sidebar.info("Running in offline demonstration mode. No API key needed.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 About Agent")
st.sidebar.markdown(
    "This agent analyzes algorithm problems, writes clean solution code in your chosen language, "
    "and breaks down the logic, complexity, and edge cases."
)

# Main Screen
st.markdown('<div class="main-title">🤖 Basic Coding Assistant Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter a coding problem description and choose your preferred language. The agent will formulate the strategy, generate code, and explain the logic.</div>', unsafe_allow_html=True)

# Example problems for quick testing
col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
example_p = None

if col_ex1.button("📌 Two Sum"):
    example_p = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume each input has exactly one solution, and you may not use the same element twice."
if col_ex2.button("📌 Reverse Linked List"):
    example_p = "Given the head of a singly linked list, reverse the list, and return the reversed list. Discuss both iterative and recursive implementations."
if col_ex3.button("📌 Valid Palindrome"):
    example_p = "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string s, return true if it is a palindrome, or false otherwise."
if col_ex4.button("📌 LRU Cache"):
    example_p = "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache with get(key) and put(key, value) in O(1) average time complexity."

# Input Form
col_lang, col_con = st.columns([1, 2])
with col_lang:
    language = st.selectbox(
        "Target Language",
        options=[
            "Python", "JavaScript", "TypeScript", "C++", "Java",
            "Go", "Rust", "C#", "Kotlin", "Swift", "PHP", "Ruby", "SQL"
        ],
        index=0
    )

with col_con:
    constraints = st.text_input(
        "Additional Constraints / Preferences (Optional)",
        placeholder="e.g. Must run in O(n) time, do in-place without extra space"
    )

default_problem_text = example_p or ""
problem_description = st.text_area(
    "Problem Description",
    value=default_problem_text,
    height=150,
    placeholder="Example: Write a function that finds the longest palindromic substring in a given string..."
)

generate_btn = st.button("🚀 Generate Solution & Explanation", type="primary", use_container_width=True)

if generate_btn:
    if not problem_description.strip():
        st.warning("⚠️ Please enter a problem description first.")
    else:
        with st.spinner(f"Agent is analyzing problem and writing {language} solution..."):
            # Initialize agent
            agent = CodingAssistantAgent(
                provider=provider_slug,
                model=model_name,
                api_key=api_key if api_key else None
            )

            result = agent.solve(
                problem=problem_description,
                language=language.lower(),
                constraints=constraints if constraints.strip() else None
            )

            if result.get("success"):
                is_mock = result.get("is_mock", False)
                if is_mock:
                    st.markdown('<span class="badge badge-mock">Offline Mock Mode</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="badge badge-live">Live Response: {result.get("provider").title()} ({result.get("model")})</span>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown(result["response"])
            else:
                st.error("❌ Failed to generate solution:")
                st.write(result.get("error"))
                if "fallback_advice" in result:
                    st.info(result["fallback_advice"])
