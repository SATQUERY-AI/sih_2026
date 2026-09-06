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
You are the Intent Classifier for SatQuery AI.

SatQuery AI is a remote-sensing vision-language assistant.

Classify the query into exactly one intent:

single_image:
Query requires one optical or SAR image.

bi_temporal:
Query requires two images from different times
(before/after comparison).

cross_modal:
Query requires both optical and SAR images together.

Return ONLY JSON:

{
 "intent":"single_image | bi_temporal | cross_modal",
 "query_type":"vqa | change_analysis | cross_modal_analysis",
 "reason":"short explanation"
}

Do not use keyword matching.
Understand the meaning of the query.
"""


def classify_intent(query: str) -> dict:

    query = query.strip()

    if not query:
        return {
            "valid": False,
            "intent": None,
            "query_type": None,
            "reason": "Empty query",
            "message": "Invalid query"
        }


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }


    payload = {

        "model": MODEL_NAME,

        "messages":[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":query
            }
        ],

        "temperature":0,

        "max_tokens":100
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

            content = content.replace("```json","")
            content = content.replace("```","")
            content = content.strip()


        data = json.loads(content)



        return {

            "valid":True,

            "query":query,

            "intent":data["intent"],

            "query_type":data["query_type"],

            "reason":data["reason"],

            "message":
            "Intent classified successfully."
        }


    except Exception as e:

        return {

            "valid":False,

            "query":query,

            "intent":None,

            "query_type":None,

            "reason":None,

            "message":
            f"Intent classification failed: {str(e)}"

        }