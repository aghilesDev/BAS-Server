import requests
import sys

print(sys.argv[1])
payload = {
        "task_id": sys.argv[1],
}
headers = {
    "Content-Type": "application/json"
    }

url = "http://127.0.0.1:5000/webhook/clickupPostCreated"
response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)