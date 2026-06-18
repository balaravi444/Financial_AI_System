import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are FinanceAI, an expert Indian financial advisor and 
stock market analyst. You follow all SEBI and NSE rules. You explain everything 
clearly — how stocks work, mutual funds, FDs, insurance, savings tips, and 
investment planning. You always give step-by-step reasoning before any 
recommendation. You always remind users that this is educational information 
and not SEBI-registered investment advice."""

conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def ask_finance_ai(user_question):
    from groq.types.chat import ChatCompletionMessageParam
    conversation_history.append({
        "role": "user",
        "content": user_question
    })


    # Build messages list using a list comprehension for correct type
    from groq.types.chat import ChatCompletionMessageParam
    from typing import cast
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    for msg in conversation_history[1:]:
        messages.append(cast(ChatCompletionMessageParam, msg))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024,
        temperature=0.7
    )

    reply = response.choices[0].message.content or ""

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

def main():
    print("=" * 50)
    print("Welcome to FinanceAI — Your Smart Money Guide")
    print("Powered by Groq + LLaMA 3.3 70B")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye! Invest wisely.")
            break

        if not user_input:
            continue

        print("\nFinanceAI: Thinking...\n")

        try:
            response = ask_finance_ai(user_input)
            print(f"FinanceAI: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()