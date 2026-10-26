import re
from pathlib import Path

TOOL_PROMPT = """
You are a helpful assistant that can list folders and read and write files.
Only use a tool when the user asks you to list a folder or read or write a file.
For anything else, like greetings or questions, just reply normally without any tags.

You use the tools yourself. The user cannot use them, so never ask the user to write a tag.
To use a tool, write the tag in your reply. Nothing happens unless you write the tag.
Replace PATH with the path the user gave you, and TEXT with the file contents.

To list a folder:
<ls PATH>
If the user says "this folder" or does not name a folder, use . as the PATH, like <ls .>

To read a file:
<read PATH>

To write a file:
<write PATH>TEXT</write>

After writing a tag, stop your reply. You get the result in the next message.
Never say you listed, read or wrote anything unless you used the tag.
"""

LS = re.compile(r"<ls(?: (.+?))?>")
READ = re.compile(r"<read (.+?)>")
WRITE = re.compile(r"<write (.+?)>(.*?)</write>", re.DOTALL)

def list_dir(path: str) -> str:
    entries = sorted(Path(path).iterdir())
    names = [entry.name + "/" if entry.is_dir() else entry.name for entry in entries]
    return "\n".join(names) or "(empty folder)"

def read_file(path: str) -> str:
    return Path(path).read_text()

def write_file(path: str, content: str) -> str:
    Path(path).write_text(content)
    return f"Wrote {path}"

def match_tool(text: str) -> str | None:
    try:
        if match := LS.search(text):
            return list_dir((match[1] or ".").strip("\"'"))
        if match := READ.search(text):
            return read_file(match[1].strip("\"'"))
        if match := WRITE.search(text):
            return write_file(match[1].strip("\"'"), match[2])
    except OSError as error:
        return f"Error: {error}"
    return None
