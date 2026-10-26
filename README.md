# dolphin_mistral_tools

`dolphin-mistral` is an older model without native tool support, so this project works around it by having the model write tags that the code then runs as tools.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com), running
- The model: `ollama pull dolphin-mistral`

## Run

```sh
uv run model
```

## Tools

- `<read PATH>` reads a file
- `<write PATH>TEXT</write>` writes a file
- `<ls PATH>` lists a folder
- `<find NAME PATH>` finds a file
