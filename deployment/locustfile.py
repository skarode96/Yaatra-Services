from locust import HttpLocust, TaskSet, task, between
import json
import logging
logger = logging.getLogger(__name__)

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("/user/login/",
                                    {"username": "admin",
                                         "password": "qwerty1234"})
        response_json = json.loads(response.text)
        self.token_key = "Token " + response_json["authToken"]
        if response.status_code == 200:
            logger.debug("response from host for currency" + response.text)

    @task(1)
    def get_daily_commutes(self):
        daily_commutes = self.client.post("/commute/daily/details/",
                                        headers={"Authorization": self.token_key},
                                        data={"journey_id": 0})
        print(daily_commutes)
        #daily_commutes_json = json.loads(daily_commutes.text)
        #print(daily_commutes_json.text)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 3)
