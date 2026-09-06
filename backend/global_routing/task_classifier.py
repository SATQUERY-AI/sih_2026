import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemini-2.5-flash"
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


SYSTEM_PROMPT = """
You are the Task Classifier for SatQuery AI.

SatQuery AI is an agentic remote-sensing vision-language
assistant for analysing optical, SAR, and bi-temporal imagery.

The Global Intent Classifier has already determined the
broad intent.

Your task is to determine the specific task required.

Do NOT use keyword matching.
Understand the complete meaning of the user's query.

Allowed tasks:

For single_image:

- vqa
  Answer a question about one image.

- captioning
  Generate a description of one image.

- grounding
  Identify or locate an object or feature in one image.

For bi_temporal:

- change_detection
  Detect whether changes occurred between two images.

- change_captioning
  Describe the changes between two images.

- change_vqa
  Answer a question about changes between two images.

For cross_modal:

- cross_modal_analysis
  Analyse optical and SAR imagery together.

Model mapping:

single_image -> GeoChat

bi_temporal -> TEMPORAL_MODEL

cross_modal -> CROMA

Do not change the provided intent.

Return ONLY valid JSON:

{
    "task": "vqa | captioning | grounding | change_detection | change_captioning | change_vqa | cross_modal_analysis",
    "model": "GeoChat | TEMPORAL_MODEL | CROMA",
    "reason": "short explanation"
}
"""


def classify_task(query: str, intent: str) -> dict:

    query = query.strip()

    if not query:
        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": "",
            "reason": "Query cannot be empty.",
            "message": "Invalid query."
        }

    valid_intents = {
        "single_image",
        "bi_temporal",
        "cross_modal"
    }

    if intent not in valid_intents:
        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": query,
            "reason": "Invalid intent.",
            "message": f"Unsupported intent: {intent}"
        }

    if not OPENROUTER_API_KEY:
        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": query,
            "reason": None,
            "message": "OPENROUTER_API_KEY is not configured."
        }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    user_message = f"""
The intent has already been classified as:

{intent}

User query:

{query}

Determine the specific task and corresponding specialist model.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0,
        "max_tokens": 100
    }

    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        content = result["choices"][0]["message"]["content"].strip()

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        classification = json.loads(content)

        task = classification.get("task")
        model = classification.get("model")
        reason = classification.get("reason", "")

        valid_tasks = {
            "vqa",
            "captioning",
            "grounding",
            "change_detection",
            "change_captioning",
            "change_vqa",
            "cross_modal_analysis"
        }

        valid_models = {
            "GeoChat",
            "TEMPORAL_MODEL",
            "CROMA"
        }

        if task not in valid_tasks:
            raise ValueError(
                f"Invalid task returned by LLM: {task}"
            )

        if model not in valid_models:
            raise ValueError(
                f"Invalid model returned by LLM: {model}"
            )

        valid_combinations = {
            "single_image": {
                "vqa",
                "captioning",
                "grounding"
            },
            "bi_temporal": {
                "change_detection",
                "change_captioning",
                "change_vqa"
            },
            "cross_modal": {
                "cross_modal_analysis"
            }
        }

        if task not in valid_combinations[intent]:
            raise ValueError(
                f"Task '{task}' is not valid for intent '{intent}'."
            )

        expected_model = {
            "single_image": "GeoChat",
            "bi_temporal": "TEMPORAL_MODEL",
            "cross_modal": "CROMA"
        }

        if model != expected_model[intent]:
            raise ValueError(
                f"Model '{model}' does not match intent "
                f"'{intent}'. Expected '{expected_model[intent]}'."
            )

        return {
            "valid": True,
            "intent": intent,
            "task": task,
            "model": model,
            "query": query,
            "reason": reason,
            "message": "Task classified successfully."
        }

    except requests.exceptions.Timeout:

        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": query,
            "reason": None,
            "message": "OpenRouter request timed out."
        }

    except requests.exceptions.HTTPError as e:

        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": query,
            "reason": None,
            "message": f"OpenRouter HTTP error: {str(e)}"
        }

    except json.JSONDecodeError:

        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": query,
            "reason": None,
            "message": "LLM returned invalid JSON."
        }

    except Exception as e:

        return {
            "valid": False,
            "intent": intent,
            "task": None,
            "model": None,
            "query": query,
            "reason": None,
            "message": f"Task classification failed: {str(e)}"
        }