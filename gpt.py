import requests

API_KEY = "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" # сюда реальный ключ

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
"Authorization": f"Bearer {API_KEY}",
"Content-Type": "application/json",
}

def text_ai(text):
    data = {
    "model": "openrouter/free",
    "messages": [
    {"role": "system", "content": "Ты полезный помощник. Отвечай на вопросы кратко и по существу."
    " "},
    {"role": "user", "content": text}
    ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    result = response.json()

    return result["choices"][0]["message"]["content"]