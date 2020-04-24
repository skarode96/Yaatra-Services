import requests
import json
import sys

API_ENDPOINT = "http://192.168.0.221:4000/user/login/"

API_ENDPOINT = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]


data = {'username':USERNAME,
        'password':PASSWORD}
count=0
while True:
	print("Request No. :", count)
	count+=1
# sending post request and saving response as response object 
	reponse = requests.post(url = API_ENDPOINT, data = data)
	if(reponse.status_code == 503):
		print("Response :%s"%reponse.text)
	else:
		reponse = json.loads(reponse.text)
		print("Response :%s"%reponse)
	
