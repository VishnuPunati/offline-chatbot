# Offline Customer Support Chatbot

This project is an offline customer support chatbot for a fictional e-commerce store. It runs on a local Ollama server with the `llama3.2:3b` model and compares zero-shot and one-shot prompting across 20 adapted customer queries.

## Overview

The application:

- loads prompt templates from `prompts/`
- processes 20 e-commerce customer support queries
- generates one zero-shot and one one-shot response for each query
- sends requests to `http://localhost:11434/api/generate`
- writes the responses to `eval/results.md` for manual scoring

## Project Structure

```text
chatbot/
|-- prompts/
|   |-- zero_shot_template.txt
|   `-- one_shot_template.txt
|-- eval/
|   `-- results.md
|-- chatbot.py
|-- setup.md
|-- report.md
`-- README.md
```

## Included Files

- `chatbot.py`
- `prompts/zero_shot_template.txt`
- `prompts/one_shot_template.txt`
- `eval/results.md`
- `setup.md`
- `report.md`
- `README.md`

## How To Run

Follow the instructions in `setup.md`, then run:

```powershell
python chatbot.py
```

The script writes its output to `eval/results.md`.

## How To Run With Docker

You can also run the project with Docker Compose:

```powershell
docker compose up --build
```

This starts:

- `ollama`, which serves the local model on port `11434`
- `chatbot`, which waits for Ollama, ensures `llama3.2:3b` is available, and runs the evaluation

When the run finishes, the generated output will be available in `eval/results.md` on your machine.

## Notes

- All inference is intended to stay local through Ollama.
- If Ollama is unavailable, the script still creates `eval/results.md` and records the connection error in the response column.
- `datasets` is included in `requirements.txt` because the assignment references the Ubuntu Dialogue Corpus, even though the final implementation uses 20 curated customer queries.
