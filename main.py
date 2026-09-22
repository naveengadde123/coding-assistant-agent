"""
CLI Interface for the Basic Coding Assistant Agent
Run interactively or with command-line flags.
"""

import sys
import argparse
from agent import CodingAssistantAgent

# Ensure UTF-8 output encoding on Windows terminals
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")



def print_banner():
    print("=" * 65)
    print("       🤖 Basic Coding Assistant Agent (CLI Interface)")
    print("=" * 65)
    print("Generates code & explains logic for any programming problem.\n")


def interactive_mode(agent: CodingAssistantAgent):
    print_banner()
    print(f"Active Provider: [{agent.provider}] (Model: {agent.model})")
    if agent.provider.startswith("mock"):
        print("💡 Hint: Add GROQ_API_KEY or OPENAI_API_KEY to a .env file to enable live AI models.\n")

    while True:
        print("-" * 65)
        print("Enter your coding problem description (or type 'exit' / 'quit' to stop):")
        lines = []
        try:
            line = input("> ").strip()
            if line.lower() in ["exit", "quit"]:
                print("\nGoodbye! Happy coding! 🚀")
                break
            if not line:
                print("Problem description cannot be empty. Try again.")
                continue
            lines.append(line)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        problem_text = "\n".join(lines)

        lang = input("\nTarget language [Default: python]: ").strip()
        if not lang:
            lang = "python"

        constraints = input("Optional constraints/notes [Press Enter to skip]: ").strip()

        print(f"\n⏳ Thinking & generating {lang.title()} solution...\n")
        result = agent.solve(problem=problem_text, language=lang, constraints=constraints or None)

        if result.get("success"):
            print("\n" + "=" * 65)
            print("                AGENT SOLUTION & EXPLANATION")
            print("=" * 65 + "\n")
            print(result["response"])
            print("\n" + "=" * 65 + "\n")
        else:
            print("\n❌ Error generating solution:")
            print(result.get("error"))
            if "fallback_advice" in result:
                print(f"👉 {result['fallback_advice']}\n")


def main():
    parser = argparse.ArgumentParser(description="Basic Coding Assistant Agent CLI")
    parser.add_argument("-p", "--problem", type=str, help="Problem description")
    parser.add_argument("-l", "--language", type=str, default="python", help="Target programming language (e.g. python, javascript, cpp, java, go, rust)")
    parser.add_argument("-c", "--constraints", type=str, default=None, help="Optional constraints or test notes")
    parser.add_argument("--provider", type=str, default=None, choices=["gemini", "groq", "openai", "mock"], help="LLM provider")
    parser.add_argument("--api-key", type=str, default=None, help="Explicit API key")

    args = parser.parse_args()

    agent = CodingAssistantAgent(provider=args.provider, api_key=args.api_key)

    if args.problem:
        print(f"Generating solution in {args.language} using [{agent.provider}]...\n")
        result = agent.solve(problem=args.problem, language=args.language, constraints=args.constraints)
        if result.get("success"):
            print(result["response"])
        else:
            print("Error:", result.get("error"))
            sys.exit(1)
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
