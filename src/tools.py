import re
from pathlib import Path

TOOL_PROMPT = """
You are a helpful assistant that can read and write files.
To use a tool, write the tag in your reply. Nothing happens unless you write the tag.

To read a file:
<read src/main.py>

To write a file:
<write notes.txt>hello</write>

After writing a tag, stop your reply. You get the result in the next message.
Never say you read or wrote a file unless you used the tag.
"""

READ = re.compile(r"<read (.+?)>")
WRITE = re.compile(r"<write (.+?)>(.*?)</write>", re.DOTALL)

def read_file(path: str) -> str:
    return Path(path).read_text()

def write_file(path: str, content: str) -> str:
    Path(path).write_text(content)
    return f"Wrote {path}"

def match_tool(text: str) -> str | None:
    try:
        if match := READ.search(text):
            return read_file(match[1])
        if match := WRITE.search(text):
            return write_file(match[1], match[2])
    except OSError as error:
        return f"Error: {error}"
    return None
