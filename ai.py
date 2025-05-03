# =========================
# UPDATED ai.py FILE CONTENT
# =========================

import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Load environment variables
ASTRA_ENDPOINT = os.getenv("ASTRA_ENDPOINT")
ASTRA_DB_TOKEN = os.getenv("ASTRA_DB_TOKEN")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

LANGFLOW_TOKEN = os.getenv("LANGFLOW_TOKEN")  # Token for Macros
ASK_AI_LANGFLOW_TOKEN = os.getenv("ASK_AI_LANGFLOW_TOKEN")  # Token for Ask AI

# Define URLs
MACROS_FLOW_URL = "https://api.langflow.astra.datastax.com/lf/e059f796-7ca7-46f9-b029-f47318f6cd03/api/v1/run/91989848-073b-409a-aaaa-f6ff1dbe904d"
ASK_AI_FLOW_URL = "https://api.langflow.astra.datastax.com/lf/e059f796-7ca7-46f9-b029-f47318f6cd03/api/v1/run/c901eceb-e74a-4ef0-ab35-19641435f852"


def run_flow(message: str,
             flow_url: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    if tweaks:
        payload.update({"tweaks": tweaks})

    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(flow_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Langflow API Error {response.status_code}: {response.text}")

    result = response.json()
    if "outputs" not in result:
        raise Exception("Unexpected Langflow API response: Missing 'outputs'")

    return json.loads(result["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])


def dict_to_string(d):
    return "\n".join([f"{k}: {v}" for k, v in d.items() if v])


def get_macros(profile, goals):
    tweaks = {
        "TextInput-PR5Jb": {"input_value": ", ".join(goals)},
        "TextInput-PrfY9": {"input_value": dict_to_string(profile)},
    }
    return run_flow(
        message="",
        flow_url=MACROS_FLOW_URL,
        tweaks=tweaks,
        application_token=LANGFLOW_TOKEN
    )


def ask_ai(profile, question):
    # API configuration
    url = "https://api.langflow.astra.datastax.com/lf/e059f796-7ca7-46f9-b029-f47318f6cd03/api/v1/run/c901eceb-e74a-4ef0-ab35-19641435f852"
    token = ASK_AI_LANGFLOW_TOKEN
    
    tweaks = {
        "TextInput-1CPBk": {
            "input_value": question
        },
        "TextInput-NEq2E": {
            "input_value": dict_to_string(profile)
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "input_type": "text",
        "output_type": "text",
        "tweaks": tweaks
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        # 🛠️ Safely extract JUST the text part
        if "outputs" in result:
            # Navigate step-by-step into nested structure
            outputs = result.get("outputs", [])
            if outputs and "outputs" in outputs[0]:
                outputs_list = outputs[0]["outputs"]
                if outputs_list and "results" in outputs_list[0]:
                    results = outputs_list[0]["results"]
                    if "text" in results and "data" in results["text"]:
                        text_data = results["text"]["data"]
                        if "text" in text_data:
                            return text_data["text"]

        # If structure unexpected, fallback to dump result
        return json.dumps(result, indent=2)

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"
    except ValueError as e:
        return f"Response Not JSON: {str(e)}"
