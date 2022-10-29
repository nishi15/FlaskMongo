import requests,datetime


url = "http://127.0.0.1:5000/"

add_notes = "http://127.0.0.1:5000/add-note"

# resp = requests.get(url)
# print(resp)

data = {
	"title":'Flask and Mongo 2',
	'description':'Testing flask APIs with MongoDB',
	'createdAt':datetime.datetime.now()
}
resp = requests.post(add_notes,data=data)
print(resp)