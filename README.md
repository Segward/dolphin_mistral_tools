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

- `<ls path>` lists a folder
- `<read path>` reads a file
- `<write path>text</write>` writes a file
