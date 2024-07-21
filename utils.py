import requests

def send_data(destination, data):
    headers = destination.headers
    if destination.http_method.lower() == "get":
        response = requests.get(destination.url, headers=headers, params=data)
    elif destination.http_method.lower() == "post":
        response = requests.post(destination.url, headers=headers, json=data)
    elif destination.http_method.lower() == "put":
        response = requests.put(destination.url, headers=headers, json=data)
    else:
        response = None
    return response

