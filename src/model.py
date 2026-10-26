from ollama import chat

from tools import TOOL_EXAMPLES, TOOL_PROMPT


def new_chat() -> list[dict]:
    return [{"role": "system", "content": TOOL_PROMPT}, *TOOL_EXAMPLES]

def ask_model(messages: list[dict], content: str) -> str:
    messages.append({"role": "user", "content": content})
    reply = chat(model="dolphin-mistral", messages=messages).message.content
    messages.append({"role": "assistant", "content": reply})
    return reply
