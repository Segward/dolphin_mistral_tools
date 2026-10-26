from model import ask_model, new_chat
from tools import match_tool


def main() -> None:
    messages = new_chat()

    try:
        while True:
            content = input("> ")
            if content == "exit":
                break

            while content is not None:
                reply = ask_model(messages, content)
                print(reply)

                result = match_tool(reply)
                content = None if result is None else f"Tool result:\n{result}"
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
