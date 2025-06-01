# knowledge_extraction.py
# import openai
import requests
import spacy
from urllib.parse import quote
from config import SPOTLIGHT_API_URL, BABELFY_API_URL, BABELFY_API_KEY, LOV_API

nlp = spacy.load("en_core_web_sm")
# export OPENAI_API_KEY="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"


def ask_the_llm(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.RequestException as e:
        return f"[ERROR] No se pudo conectar con Ollama: {e}"


def extract_triplets_llm(sentence):
    prompt = f"""
Extract RDF-style triples from the following sentence:
\"{sentence}\"

Only return the extracted RDF triples in the format:
(Subject, Predicate, Object)

Do NOT add any explanations or comments.
Do NOT return anything else.
"""
    return ask_the_llm(prompt)


def extend_text_llm(text):
    prompt = f"""
Understand the following text, and extend any contractions that exist, e.g. detect the pronouns and replace them with the real subjects:
\"{text}\"

Do NOT add any explanations or comments.
Do NOT return anything else.
"""
    return ask_the_llm(prompt)


def get_babelfy_url(text: str) -> str:
    return BABELFY_API_URL + f"text={quote(text)}&lang=EN&key={BABELFY_API_KEY}"


def get_spotlight_url(text: str) -> str:
    return SPOTLIGHT_API_URL + f"text={quote(text)}"


def entity_linking_spotlight(text):
    headers = {"accept": "application/json"}
    params = {"text": text}
    try:
        response = requests.get(
            SPOTLIGHT_API_URL,
            headers=headers,
            params=params,
            verify=True
        )
        return {r['surfaceForm']: r['URI'] for r in response.json().get('Resources', [])}
    except Exception as error:
        print(error)
        return {}


def entity_linking_babelfy(text):
    try:
        headers = {"accept": "application/json"}
        response = requests.get(get_babelfy_url(text), headers=headers)

        if (response.status_code == 200):
            data = response.json()
            max_resource = max(
                data, key=lambda resource: resource['globalScore'])
            best_resource = max_resource['DBpediaURL'] if data != [] else ''

            return best_resource

        return None
    except Exception as error:
        print(error)
        return {}


def predicate_mapping_lov(predicate):
    try:
        url = f"{LOV_API}?q={predicate}&type=property"
        response = requests.get(url)
        data = response.json()["results"]
        if data:
            return data[0].get("uri")[0]
    except Exception as error:
        print(error)
        return None
