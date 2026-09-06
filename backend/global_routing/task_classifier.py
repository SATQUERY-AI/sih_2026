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


Based on the given intent decide the task and model.


Allowed tasks:


single_image:

vqa
captioning
grounding


bi_temporal:

change_detection
change_captioning
change_vqa


cross_modal:

cross_modal_analysis



Model mapping:

single_image -> GeoChat

bi_temporal -> TEMPORAL_MODEL

cross_modal -> CROMA



Return ONLY JSON:


{
"task":"",
"model":"",
"reason":""
}

"""


def classify_task(query:str,intent:str)->dict:


    headers={

        "Authorization":
        f"Bearer {OPENROUTER_API_KEY}",

        "Content-Type":
        "application/json"
    }


    prompt=f"""

Intent:
{intent}


Query:
{query}


Choose correct task and model.

"""


    payload={

        "model":MODEL_NAME,

        "messages":[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":prompt
            }

        ],

        "temperature":0,

        "max_tokens":100
    }



    try:


        response=requests.post(

            OPENROUTER_URL,

            headers=headers,

            json=payload,

            timeout=60

        )


        response.raise_for_status()


        result=response.json()


        content=result["choices"][0]["message"]["content"].strip()


        if content.startswith("```"):

            content=content.replace("```json","")
            content=content.replace("```","")
            content=content.strip()



        data=json.loads(content)



        return {

            "valid":True,

            "intent":intent,

            "task":data["task"],

            "model":data["model"],

            "query":query,

            "reason":data["reason"],

            "message":
            "Task classified successfully."

        }



    except Exception as e:


        return {

            "valid":False,

            "intent":intent,

            "task":None,

            "model":None,

            "query":query,

            "reason":None,

            "message":
            f"Task classification failed: {str(e)}"

        }