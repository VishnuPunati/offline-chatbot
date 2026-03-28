# Setup Guide

## 1. Install Ollama

Download Ollama for your operating system from <https://ollama.com/download> and complete the installation.

## 2. Verify The Installation

```powershell
ollama --version
```

## 3. Pull The Required Model

```powershell
ollama pull llama3.2:3b
```

## 4. Optional Interactive Check

```powershell
ollama run llama3.2:3b
```

Type a short message to confirm the model is responding, then exit the session.

## 5. Create A Python Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 6. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

## 7. Start Ollama

Make sure the Ollama application or background service is running locally so that `http://localhost:11434` is available.

## 8. Run The Chatbot Experiment

```powershell
python chatbot.py
```

## 9. Review The Results

Open `eval/results.md` and manually score each response using:

- Relevance (1-5)
- Coherence (1-5)
- Helpfulness (1-5)

## Troubleshooting

- If you see a connection error, confirm that Ollama is running and listening on port `11434`.
- If the model is missing, run `ollama pull llama3.2:3b` again.
- If inference is slow, that is expected on CPU-only systems.
