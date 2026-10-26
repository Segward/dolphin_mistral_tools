import re
from pathlib import Path

TOOL_PROMPT = """
You are a helpful assistant that can use tools.
To use a tool, reply with the corresponding tag.

To read a file:
    <read PATH>

To write a file:
    <write PATH>TEXT</write>

To list a folder:
    <ls PATH>

To find files by name in a folder and all its subfolders:
    <find NAME PATH>

Keywords:
    PATH: The file path or directory path.
    TEXT: The content to write to the file.
    NAME: The full or partial filename to search for.

After writing a tool tag, stop your reply.
You will receive the tool result in the next message.
"""

READ = re.compile(r"<read (.+?)>")
WRITE = re.compile(r"<write (.+?)>(.*?)</write>", re.DOTALL)
LS = re.compile(r"<ls(?: (.+?))?>")
FIND = re.compile(r"<find (.+?)>")

def read_file(path: str) -> str:
    return Path(path).read_text()

def write_file(path: str, text: str) -> str:
    Path(path).write_text(text)
    return f"Wrote {path}"

def list_folder(path: str) -> str:
    entries = sorted(Path(path).iterdir())
    names = [entry.name + "/" if entry.is_dir() else entry.name for entry in entries]
    return "\n".join(names) or "Empty folder"

def find_file(name: str, path: str = ".") -> str:
    matches = sorted(
        str(file) for file in Path(path).rglob(f"*{name}*")
        if file.is_file()
    )
    return "\n".join(matches) or "No files found"

def match_tool(text: str) -> str | None:
    try:
        if match := READ.search(text):
            return read_file(match[1].strip("\"'"))
        if match := WRITE.search(text):
            return write_file(match[1].strip("\"'"), match[2])
        if match := LS.search(text):
            return list_folder((match[1] or ".").strip("\"'"))
        if match := FIND.search(text):
            return find_file
    except OSError as error:
        return f"Error: {error}"
    return None
