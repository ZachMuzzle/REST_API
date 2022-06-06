import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":69, "name": "Emily's first video","views": 3400},
        {"likes":34, "name": "Jim's second video","views": 1200},
        {"likes":240, "name": "Mark's fourth video","views": 24042}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i]) #update data
    print(response.json())

input()
response = requests.get(BASE + "video/1") #get data video/1 which is that data updated above
print(response.json())
input()
response = requests.patch(BASE + "video/2", {"views": 101})
print(response.json())
input()
response = requests.get(BASE + "video/2") #get data video/2 which is that data updated above
print(response.json())