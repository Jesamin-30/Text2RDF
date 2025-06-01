import requests

def prompt_ollama(prompt, model='llama3'):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Si quieres respuesta completa (no en partes)
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.RequestException as e:
        return f"[ERROR] No se pudo conectar con Ollama: {e}"

# Ejemplo de uso
if __name__ == "__main__":
    prompt = "Extract triples in RDF format from this sentence: 'Alan Turing developed the Turing machine.'"
    output = prompt_ollama(prompt)
    print("Respuesta del modelo Ollama:")
    print(output)
