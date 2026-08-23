import requests

def get_wikipedia_summary(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    headers = {"User-Agent": "SmartKBAssistant/1.0 (student project)"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Error: couldn't find information on '{topic}' (status {response.status_code})"

    data = response.json()
    return data.get("extract", "No summary available.")

if __name__ == "__main__":
    result = get_wikipedia_summary("Python_(programming_language)")
    print(result)
