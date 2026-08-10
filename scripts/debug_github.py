import requests

USERNAME = "Adarshit007"

URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=headers,
    timeout=30
)

print("HTTP:", response.status_code)
print("HTML length:", len(response.text))

with open(
    "github_debug.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(response.text)

print()
print("Saved: github_debug.html")