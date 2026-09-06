import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemini-2.5-flash"
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ---------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are the Global Intent Classifier for SatQuery AI.

SatQuery AI is an agentic remote-sensing vision-language
assistant for analysing optical, SAR, and bi-temporal
remote-sensing imagery.

Your task is to understand the COMPLETE meaning of the
user's query and classify it into EXACTLY ONE intent.

---------------------------------------------------------
INTENT 1: single_image
---------------------------------------------------------

Use this when the query requires analysis of ONE image.

The image can be:
- Optical
- Multispectral
- SAR

Examples:

"What is the main feature in this image?"

"How many buildings are present?"

"Is this an urban area?"

"Identify the land cover in the image."

"Is there a road in the image?"

---------------------------------------------------------
INTENT 2: bi_temporal
---------------------------------------------------------

Use this when the query requires analysis of TWO images
from DIFFERENT TIMES.

This includes:
- Before/after comparison
- Temporal change detection
- Change description
- Questions about what appeared or disappeared
- Questions about increase/decrease over time

Examples:

"What changed between the before and after images?"

"Has the vegetation changed?"

"Describe the changes between these two dates."

"Did new buildings appear?"

"Has the road network changed?"

---------------------------------------------------------
INTENT 3: cross_modal
---------------------------------------------------------

Use this when the query requires BOTH OPTICAL and SAR
imagery together.

This includes:
- Optical + SAR comparison
- Joint optical-SAR analysis
- Questions requiring information from both modalities

Examples:

"Compare the optical and SAR images."

"Analyze the scene using both optical and SAR data."

"What differences can be observed between optical and SAR?"

"What does the SAR image reveal compared with the optical image?"

---------------------------------------------------------
IMPORTANT RULES
---------------------------------------------------------

1. Understand the complete meaning of the query.

2. Do NOT use simple keyword matching.

3. Do NOT classify based on one word.

4. Determine which type of imagery is required by the
   actual meaning of the query.

5. Return EXACTLY ONE intent.

6. Return ONLY valid JSON.

The JSON must have exactly these fields:

{
    "intent": "single_image | bi_temporal | cross_modal",
    "query_type": "vqa | change_analysis | cross_modal_analysis",
    "reason": "short explanation"
}

---------------------------------------------------------
EXAMPLE 1
---------------------------------------------------------

User:
What is the main feature in this image?

Output:
{
    "intent": "single_image",
    "query_type": "vqa",
    "reason": "The query requires analysis of a single image."
}

---------------------------------------------------------
EXAMPLE 2
---------------------------------------------------------

User:
What changed between the before and after images?

Output:
{
    "intent": "bi_temporal",
    "query_type": "change_analysis",
    "reason": "The query requires comparison of imagery from different times."
}

---------------------------------------------------------
EXAMPLE 3
---------------------------------------------------------

User:
Compare the optical and SAR images.

Output:
{
    "intent": "cross_modal",
    "query_type": "cross_modal_analysis",
    "reason": "The query requires both optical and SAR imagery."
}
"""


# ---------------------------------------------------------
# CLASSIFY INTENT
# ---------------------------------------------------------

def classify_intent(query: str) -> dict:

    # Clean query
    query = query.strip()

    # -----------------------------------------------------
    # Validate query
    # -----------------------------------------------------

    if not query:
        return {
            "valid": False,
            "intent": None,
            "query": "",
            "query_type": None,
            "reason": "Query cannot be empty.",
            "message": "Invalid query."
        }

    # -----------------------------------------------------
    # Check API key
    # -----------------------------------------------------

    if not OPENROUTER_API_KEY:
        return {
            "valid": False,
            "intent": None,
            "query": query,
            "query_type": None,
            "reason": None,
            "message": "OPENROUTER_API_KEY is not configured."
        }

    # -----------------------------------------------------
    # Headers
    # -----------------------------------------------------

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # -----------------------------------------------------
    # Payload
    # -----------------------------------------------------

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0,
        "max_tokens": 100
    }

    # -----------------------------------------------------
    # Call OpenRouter
    # -----------------------------------------------------

    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        # Raise error for HTTP failures
        response.raise_for_status()

        # -------------------------------------------------
        # Parse API response
        # -------------------------------------------------

        result = response.json()

        content = result["choices"][0]["message"]["content"].strip()

        # -------------------------------------------------
        # Remove markdown code fences
        # -------------------------------------------------

        if content.startswith("```"):

            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        # -------------------------------------------------
        # Parse LLM JSON
        # -------------------------------------------------

        classification = json.loads(content)

        # -------------------------------------------------
        # Extract values
        # -------------------------------------------------

        intent = classification.get("intent")
        query_type = classification.get("query_type")
        reason = classification.get("reason", "")

        # -------------------------------------------------
        # Validate intent
        # -------------------------------------------------

        valid_intents = {
            "single_image",
            "bi_temporal",
            "cross_modal"
        }

        if intent not in valid_intents:

            raise ValueError(
                f"Invalid intent returned by LLM: {intent}"
            )

        # -------------------------------------------------
        # Validate query type
        # -------------------------------------------------

        valid_query_types = {
            "vqa",
            "change_analysis",
            "cross_modal_analysis"
        }

        if query_type not in valid_query_types:

            raise ValueError(
                f"Invalid query type returned by LLM: {query_type}"
            )

        # -------------------------------------------------
        # Return successful result
        # -------------------------------------------------

        return {
            "valid": True,
            "intent": intent,
            "query": query,
            "query_type": query_type,
            "reason": reason,
            "message": "Query intent classified successfully."
        }

    # -----------------------------------------------------
    # Timeout error
    # -----------------------------------------------------

    except requests.exceptions.Timeout:

        return {
            "valid": False,
            "intent": None,
            "query": query,
            "query_type": None,
            "reason": None,
            "message": "OpenRouter request timed out."
        }

    # -----------------------------------------------------
    # HTTP error
    # -----------------------------------------------------

    except requests.exceptions.HTTPError as e:

        return {
            "valid": False,
            "intent": None,
            "query": query,
            "query_type": None,
            "reason": None,
            "message": f"OpenRouter HTTP error: {str(e)}"
        }

    # -----------------------------------------------------
    # Invalid JSON from LLM
    # -----------------------------------------------------

    except json.JSONDecodeError:

        return {
            "valid": False,
            "intent": None,
            "query": query,
            "query_type": None,
            "reason": None,
            "message": "LLM returned invalid JSON."
        }

    # -----------------------------------------------------
    # Other errors
    # -----------------------------------------------------

    except Exception as e:

        return {
            "valid": False,
            "intent": None,
            "query": query,
            "query_type": None,
            "reason": None,
            "message": f"Intent classification failed: {str(e)}"
        }