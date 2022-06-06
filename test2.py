import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/helloworld/emily") #get /helloworld from main.py. Info that is sent to client
print(response.json())

response = requests.put(BASE + "/video/0", {"likes": 10, "name": "My first video", "views": 100})
print(response.json())
input()
response = requests.get(BASE + "/video/0")
print(response.json())