from groq import Groq
from app.config import GROQ_API_KEY
from app.agent.memory import get_memory, save_memory
from app.agent.tools import TOOLS

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are an intelligent AI agent.

You have access to tools:
- retriever(query)
- calculator(expression)

If you need a tool, respond EXACTLY in this format:

TOOL: tool_name
INPUT: input_here

Otherwise respond normally.
"""

def run_agent(session_id: str, user_input: str):
    memory = get_memory(session_id)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += memory
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.2,
    )

    reply = response.choices[0].message.content.strip()

    # Tool call detected
    if reply.startswith("TOOL:"):
        lines = reply.split("\n")
        tool_name = lines[0].replace("TOOL:", "").strip()
        tool_input = lines[1].replace("INPUT:", "").strip()

        if tool_name in TOOLS:
            tool_result = TOOLS[tool_name](tool_input)

            # Append tool interaction
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "assistant", "content": f"Tool Result: {tool_result}"})

            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.2,
            )

            final_answer = final_response.choices[0].message.content.strip()

            messages.append({"role": "assistant", "content": final_answer})
            save_memory(session_id, messages[1:])

            return final_answer

    # Normal response
    messages.append({"role": "assistant", "content": reply})
    save_memory(session_id, messages[1:])
    return reply
