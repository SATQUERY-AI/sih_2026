import os
import json
import httpx


SGLANG_URL = os.getenv(
    "SGLANG_URL",
    "http://localhost:30000"
)

MODEL_NAME = os.getenv(
    "LLM_MODEL",
    "Qwen/Qwen2.5-7B-Instruct"
)


SYSTEM_PROMPT = """
You are the intent classifier for SatQuery AI, an agentic
remote-sensing vision-language assistant.

Classify the user's query into exactly ONE intent:

1. single_image
   Questions about one optical or SAR image.
   Examples: object identification, counting, scene understanding,
   land-cover questions, VQA.

2. bi_temporal
   Questions requiring comparison of an earlier/before image
   and a later/after image, especially change detection or
   change description.

3. cross_modal
   Questions requiring both optical and SAR imagery together,
   including comparison or joint analysis of the two modalities.

Return ONLY valid JSON in this format:

{
    "intent": "single_image | bi_temporal | cross_modal",
    "query_type": "vqa | change_analysis | cross_modal_analysis",
    "reason": "short explanation"
}

Do not return markdown.
Do not return any additional text.
"""


async def classify_intent(query: str) -> dict:
    query = query.strip()

    if not query:
        return {
            "valid": False,
            "intent": None,
            "query_type": None,
            "reason": "Query cannot be empty."
        }

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
        "response_format": {
            "type": "json_object"
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{SGLANG_URL}/v1/chat/completions",
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            content = result["choices"][0]["message"]["content"]

            classification = json.loads(content)

            return {
                "valid": True,
                "query": query,
                "intent": classification.get("intent"),
                "query_type": classification.get("query_type"),
                "reason": classification.get("reason"),
                "message": "Query intent classified successfully."
            }

    except Exception as e:
        return {
            "valid": False,
            "query": query,
            "intent": None,
            "query_type": None,
            "reason": None,
            "message": f"Intent classification failed: {str(e)}"
        }