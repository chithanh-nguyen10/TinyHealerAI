import requests

url = "http://127.0.0.1:8000/diagnostic"

payload = {
    "symptoms": ["eye02", "urinary01", "lung01", "digest01"],
    "anamnesis": ["digest01", "ent01"],
    "familyanamnesis": ["digest01"]
}

headers = {
    "Content-Type": "application/json",
    "token" : "super_secret_token"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print("Request failed with status code:", response.status_code)
    print("Response:", response.text)


# update_res = requests.get("http://127.0.0.1:8000/update")

# if update_res.status_code == 200:
#     hello_result = update_res.json()
#     print(hello_result)
# else:
#     print("Request failed with status code:", update_res.status_code)
#     print("Response:", update_res.text)