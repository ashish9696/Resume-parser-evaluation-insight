import ollama

def get_llm_response(prompt):
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]