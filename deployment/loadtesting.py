import requests
import json
import sys

API_ENDPOINT = "http://192.168.0.221:4000/user/login/"

API_ENDPOINT = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]

'''
http://192.168.0.221:4000/user/login/ admin qwerty1234
'''

data = {'username':USERNAME,
        'password':PASSWORD}

while True:
# sending post request and saving response as response object 
	reponse = requests.post(url = API_ENDPOINT, data = data)
	if(reponse.status_code != 200):
		print("Access Restricted")
	else:
		reponse = json.loads(reponse.text)
		print("Response :%s"%reponse)
	'''
	daily_commutes = requests.post("http://localhost:4000/commute/daily/details/",
									 headers={"Authorization": "Token 9c901606cbe98235cd3599680ae2c26b1881fdb7"},
									 data={"journey_id": 0})
	'''
