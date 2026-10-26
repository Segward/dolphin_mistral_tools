import re
from pathlib import Path

TOOL_PROMPT = f"""
You are a helpful assistant that can use tools.
The current working directory is {Path.cwd()}.
To use a tool, reply with its tag.

To read a file:
    <read PATH>

To write TEXT to a file:
    <write PATH>TEXT</write>

To list a folder:
    <ls PATH>

To list a folder and all its subfolders:
    <tree PATH>

To find files whose name contains NAME, in PATH and its subfolders:
    <find NAME PATH>

Rules:
    You know nothing about the files here, so never guess.
    For any question about files, reply with only one tool tag.
    Write nothing after the tag. The tool result comes in the next message.
"""

TOOL_EXAMPLES = [
    {"role": "user", "content": "where is notes.txt"},
    {"role": "assistant", "content": "<find notes.txt .>"},
    {"role": "user", "content": "Tool result:\nNo files found"},
    {"role": "assistant", "content": "I could not find notes.txt."},
    {"role": "user", "content": "what is in todo.md"},
    {"role": "assistant", "content": "<read todo.md>"},
    {"role": "user", "content": "Tool result:\n- buy milk"},
    {"role": "assistant", "content": "todo.md contains one item: buy milk."},
]

READ = re.compile(r"<read (.+?)>")
WRITE = re.compile(r"<write (.+?)>(.*?)</write>", re.DOTALL)
LS = re.compile(r"<ls(?: (.+?))?>")
TREE = re.compile(r"<tree(?: (.+?))?>")
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

def list_tree(path: str) -> str:
    root = Path(path)
    names = []

    for p in sorted(root.rglob("*")):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue

        name = str(p.relative_to(root))
        names.append(name + "/" if p.is_dir() else name)

    return "\n".join(names) or "Empty folder"


def find_file(name: str, path: str = ".") -> str:
    matches = []

    for file in sorted(Path(path).rglob(f"*{name}*")):
        if file.is_file() and not any(part.startswith(".") for part in file.parts):
            matches.append(str(file))

    return "\n".join(matches) or "No files found"

def match_tool(text: str) -> str | None:
    try:
        if match := READ.search(text):
            return read_file(match[1].strip("\"'"))
        if match := WRITE.search(text):
            return write_file(match[1].strip("\"'"), match[2])
        if match := LS.search(text):
            return list_folder((match[1] or ".").strip("\"'"))
        if match := TREE.search(text):
            return list_tree((match[1] or ".").strip("\"'"))
        if match := FIND.search(text):
            name, _, path = match[1].partition(" ")
            return find_file(name.strip("\"'"), (path or ".").strip("\"'"))
    except OSError as error:
        return f"Error: {error}"
    return None
