"""
Coding Assistant Agent: Core Agent Logic
Takes a coding problem description, generates optimized solution code in a specified language,
and explains the logic, complexity, and edge cases.
Supports Google Gemini, Groq, OpenAI, and an offline demonstration mode.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


SYSTEM_PROMPT = """You are an expert Senior Software Engineer and Algorithmic Coding Assistant.
Your mission is to help developers solve coding problems with high-quality, production-ready code.

When presented with a coding problem and a target programming language, you must provide:
1. **Approach & Strategy**: A concise overview of how you plan to solve the problem and which data structures/algorithms will be used.
2. **Solution Code**: Clean, idiomatic, fully functional, and well-commented code in the requested language. Include type hints and docstrings/comments where applicable.
3. **Detailed Logic Explanation**: Step-by-step breakdown of how the code works.
4. **Complexity Analysis**: Explicitly state the Time Complexity and Space Complexity with Big-O notation, accompanied by a brief rationale.
5. **Edge Cases & Testing**: Key boundary conditions handled (e.g., empty input, single element, negative numbers, overflow) and example test inputs/outputs.

Format your response cleanly in Markdown with clear section headings.
"""


class CodingAssistantAgent:
    """
    Agent that orchestrates prompt formatting, calls LLM providers (Gemini, Groq, OpenAI),
    and returns solution code and logic explanations.
    """

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the agent with preferred provider and model.
        Providers supported: 'gemini', 'groq', 'openai', 'mock' (offline fallback).
        """
        self.provider = (provider or os.getenv("DEFAULT_PROVIDER") or "").strip().lower()
        self.api_key = api_key
        self.model = model
        self.client = None
        self._setup_client()

    def _setup_client(self):
        """Configure LLM client based on available API keys or provider preference."""
        gemini_key = self.api_key or os.getenv("GEMINI_API_KEY")
        groq_key = self.api_key or os.getenv("GROQ_API_KEY")
        openai_key = self.api_key or os.getenv("OPENAI_API_KEY")

        # 1. Check Gemini
        if self.provider == "gemini" or (not self.provider and gemini_key):
            try:
                if not gemini_key or gemini_key == "your_gemini_api_key_here":
                    raise ValueError("Gemini API key not configured in .env file.")
                from google import genai
                self.client = genai.Client(api_key=gemini_key)
                self.provider = "gemini"
                self.model = self.model or "gemini-3.6-flash"
                return
            except Exception as e:
                # If key is missing or invalid, fallback to other options or mock
                if self.provider == "gemini":
                    self.init_error = str(e)

        # 2. Check Groq
        if self.provider == "groq" or (not self.provider and groq_key):
            try:
                if not groq_key or groq_key == "your_groq_api_key_here":
                    raise ValueError("Groq API key not configured.")
                from groq import Groq
                self.client = Groq(api_key=groq_key)
                self.provider = "groq"
                self.model = self.model or "llama-3.3-70b-versatile"
                return
            except Exception:
                pass

        # 3. Check OpenAI
        if self.provider == "openai" or (not self.provider and openai_key):
            try:
                if not openai_key or openai_key == "your_openai_api_key_here":
                    raise ValueError("OpenAI API key not configured.")
                from openai import OpenAI
                self.client = OpenAI(api_key=openai_key)
                self.provider = "openai"
                self.model = self.model or "gpt-4o-mini"
                return
            except Exception:
                pass

        # 4. Fallback to mock if no active credentials
        self.provider = "mock"
        self.model = "offline-mock-agent"
        self.client = None

    def solve(self, problem: str, language: str = "python", constraints: Optional[str] = None) -> Dict[str, Any]:
        """
        Takes problem description and target language, and returns structured solution.
        """
        if not problem.strip():
            raise ValueError("Problem description cannot be empty.")

        language = language.strip().lower() if language else "python"

        user_prompt = f"""Coding Problem:
{problem.strip()}

Target Language: {language}
"""
        if constraints:
            user_prompt += f"\nConstraints / Extra Requirements:\n{constraints.strip()}"

        if self.provider == "mock":
            return self._generate_mock_solution(problem, language)

        try:
            if self.provider == "gemini":
                from google.genai import types
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2,
                    ),
                )
                content = response.text
            elif self.provider in ["groq", "openai"]:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                )
                content = response.choices[0].message.content
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

            return {
                "success": True,
                "provider": self.provider,
                "model": self.model,
                "language": language,
                "response": content,
            }
        except Exception as e:
            return {
                "success": False,
                "provider": self.provider,
                "model": self.model,
                "error": str(e),
                "fallback_advice": f"Ensure your {self.provider.upper()}_API_KEY is correctly set in your .env file."
            }

    def _generate_mock_solution(self, problem: str, language: str) -> Dict[str, Any]:
        """
        Provides a demonstration response when running offline without an API key.
        """
        lang_comment = "#" if language in ["python", "ruby", "bash"] else "//"
        mock_code = {
            "python": f'''def solve_problem(input_data):\n    """\n    Solution for: {problem.strip()[:40]}...\n    """\n    # Process input\n    result = input_data\n    return result\n\n# Example usage\nif __name__ == "__main__":\n    test_input = [1, 2, 3]\n    print("Result:", solve_problem(test_input))\n''',
            "javascript": f'''/**\n * Solution for: {problem.strip()[:40]}...\n */\nfunction solveProblem(inputData) {{\n    // Process input\n    const result = inputData;\n    return result;\n}}\n\n// Example usage\nconsole.log("Result:", solveProblem([1, 2, 3]));\n''',
            "java": f'''public class Solution {{\n    // Solution for: {problem.strip()[:40]}...\n    public static Object solveProblem(Object inputData) {{\n        return inputData;\n    }}\n\n    public static void main(String[] args) {{\n        System.out.println("Result: " + solveProblem("Test"));\n    }}\n}}\n''',
            "cpp": f'''#include <iostream>\n#include <vector>\n\n// Solution for: {problem.strip()[:40]}...\nvoid solveProblem() {{\n    std::cout << "Executed solution logic" << std::endl;\n}}\n\nint main() {{\n    solveProblem();\n    return 0;\n}}\n'''
        }.get(language, f'''{lang_comment} Solution for: {problem.strip()[:40]}...\n{lang_comment} Target language: {language}\n''')

        mock_markdown = f"""### ⚠️ Offline Demonstration Mode (No API key detected)
*To connect live AI models, add `GEMINI_API_KEY` in your `.env` file (Get one free at https://aistudio.google.com).*

---

### 1. Approach & Strategy
1. **Analyze Input**: Understand the specifications given in the problem: *"{problem.strip()}"*.
2. **Algorithm Selection**: Identify optimal data structures (e.g. Hash Maps, Two Pointers, or Dynamic Programming) to satisfy time constraints.
3. **Execution**: Implement clean, idiomatic code in **{language.title()}**.

---

### 2. Solution Code ({language.title()})

```{language}
{mock_code}
```

---

### 3. Logic Explanation
1. **Input Parsing**: Handles the incoming data and initializes required storage variables.
2. **Core Computation**: Executes the algorithmic transformation step-by-step.
3. **Return Value**: Produces the expected result matching the specification.

---

### 4. Complexity Analysis
- **Time Complexity**: $O(N)$ — Linear scan through the input elements.
- **Space Complexity**: $O(1)$ — Minimal auxiliary space used.

---

### 5. Edge Cases Handled
- Empty or `null` inputs.
- Single-element collections.
- Boundary conditions and unexpected data formats.
"""
        return {
            "success": True,
            "provider": "mock (offline mode)",
            "model": "offline-mock-agent",
            "language": language,
            "response": mock_markdown,
            "is_mock": True
        }
