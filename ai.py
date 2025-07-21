import requests

def get_ai_suggestions(text):
    url = "https://api.languagetool.org/v2/check"
    data = {
        "text": text,
        "language": "en-US"
    }
    try:
        res = requests.post(url, data=data)
        res.raise_for_status()
        matches = res.json().get("matches", [])
        return [m['message'] for m in matches]
    except Exception as e:
        print("AI Suggestion Error:", e)
        return ["Error getting suggestions"]
