from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import requests


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_URL = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"
EVAL_DIR = BASE_DIR / "eval"
RESULTS_PATH = EVAL_DIR / "results.md"


@dataclass(frozen=True)
class AdaptedQuery:
    original_technical_query: str
    customer_query: str


ADAPTED_QUERIES: list[AdaptedQuery] = [
    AdaptedQuery("My wifi driver is not working after the latest update.", "My discount code is not working at checkout."),
    AdaptedQuery("How do I check the logs for the apache server?", "How do I track the shipping status of my recent order?"),
    AdaptedQuery("The package manager says dependency resolution failed.", "My payment failed, but the amount was deducted from my bank account."),
    AdaptedQuery("How do I roll back to the previous kernel version?", "Can I change my delivery address after placing my order?"),
    AdaptedQuery("The system says the file I need does not exist.", "My order confirmation email never arrived. What should I do?"),
    AdaptedQuery("Why does the installer stop halfway through setup?", "Why was my order cancelled before it shipped?"),
    AdaptedQuery("How can I recover my account after forgetting the password?", "How can I reset the password for my store account?"),
    AdaptedQuery("The backup completed, but I cannot restore my data.", "My refund was approved, but I still have not received the money."),
    AdaptedQuery("A recent patch caused the application to crash on startup.", "The app crashes whenever I try to complete checkout."),
    AdaptedQuery("Can I move the database to a different server after deployment?", "Can I change the shipping method after I place my order?"),
    AdaptedQuery("The status page says the job finished, but the output is missing.", "My order says delivered, but I cannot find the package."),
    AdaptedQuery("How do I remove a duplicate package installation?", "I was charged twice for the same order. How can this be fixed?"),
    AdaptedQuery("The remote server is timing out during sync.", "Why is my package delayed even though it shipped days ago?"),
    AdaptedQuery("How do I open a support ticket for a billing issue?", "How can I contact customer support about a billing issue?"),
    AdaptedQuery("Can I replace a faulty component with a different model?", "Can I exchange my item for a different size or color?"),
    AdaptedQuery("The authentication token expired before I finished the task.", "My checkout session expired before I could pay. Can I recover my cart?"),
    AdaptedQuery("The monitoring alert says the service is unavailable in my region.", "Do you offer international shipping to my country?"),
    AdaptedQuery("How do I cancel a scheduled job that has not started yet?", "How do I cancel an order that has not shipped yet?"),
    AdaptedQuery("The system accepted only one configuration flag at a time.", "Can I use more than one discount code on a single order?"),
    AdaptedQuery("I downloaded the wrong build. How do I replace it with the correct one?", "I received the wrong item in my package. What should I do?"),
]


def load_prompt_template(template_name: str) -> str:
    template_path = PROMPTS_DIR / template_name
    return template_path.read_text(encoding="utf-8").strip()


def build_prompt(template: str, query: str) -> str:
    return template.format(query=query)


def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"[ERROR] Failed to reach Ollama at {OLLAMA_API_URL}: {exc}"

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        return f"[ERROR] Ollama returned invalid JSON: {exc}"

    return data.get("response", "").strip() or "[ERROR] Ollama returned an empty response."


def escape_markdown_cell(value: str) -> str:
    single_line = " ".join(value.strip().split())
    return single_line.replace("|", "\\|")


def build_results_markdown(zero_template: str, one_template: str) -> str:
    lines: list[str] = [
        "# Evaluation Results",
        "",
        f"Model: `{MODEL_NAME}`",
        f"Endpoint: `{OLLAMA_API_URL}`",
        "",
        "## Scoring Rubric",
        "",
        "- Relevance (1-5): How directly the response answers the customer query.",
        "- Coherence (1-5): How clear, grammatically correct, and easy to follow the response is.",
        "- Helpfulness (1-5): How actionable and practically useful the response is.",
        "",
        "## Query Adaptation Notes",
        "",
        "The following 20 customer queries were adapted from technical-style support prompts into e-commerce scenarios, as required by the task.",
        "",
        "| Query # | Original Technical Query | Adapted Customer Query |",
        "| --- | --- | --- |",
    ]

    for index, query in enumerate(ADAPTED_QUERIES, start=1):
        lines.append(
            f"| {index} | {escape_markdown_cell(query.original_technical_query)} | {escape_markdown_cell(query.customer_query)} |"
        )

    lines.extend(
        [
            "",
            "## Logged Results",
            "",
            "| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for index, query in enumerate(ADAPTED_QUERIES, start=1):
        zero_response = query_ollama(build_prompt(zero_template, query.customer_query))
        one_response = query_ollama(build_prompt(one_template, query.customer_query))

        lines.append(
            f"| {index} | {escape_markdown_cell(query.customer_query)} | Zero-Shot | {escape_markdown_cell(zero_response)} |  |  |  |"
        )
        lines.append(
            f"| {index} | {escape_markdown_cell(query.customer_query)} | One-Shot | {escape_markdown_cell(one_response)} |  |  |  |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    EVAL_DIR.mkdir(parents=True, exist_ok=True)

    zero_template = load_prompt_template("zero_shot_template.txt")
    one_template = load_prompt_template("one_shot_template.txt")

    results_markdown = build_results_markdown(zero_template, one_template)
    RESULTS_PATH.write_text(results_markdown, encoding="utf-8")

    print(f"Saved evaluation results to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
