from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': """Extract RDF-style triples from the following sentence:
"Ciudad Victoria is a town located in the state of Tamaulipas."

Only return the extracted RDF triples in the format:
(Subject, Predicate, Object)

Do NOT add any explanations or comments.
Do NOT return anything else.""",
    },
])
print(response['message']['content'], "\n")
# or access fields directly from the response object
print(response.message.content)
