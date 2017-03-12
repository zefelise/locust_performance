import json
from locust import HttpLocust, TaskSet, task, events

class UserBehavior(TaskSet):

    @task(1)
    def version(self):
        with self.client.get("/api/version", catch_response=True) as response:
            if response.json()['version'] != "0.0.1":
                response.failure("Version not correct!")
            else:
                response.success()


    @task(5)
    def read_all(self):
        with self.client.get("/api/data", catch_response=True) as response:
            if len(response.json()) > 0:
                response.success()
            else:
                response.failure()


    @task(5)
    def read_specific_data(self):
        with self.client.get("/api/data/58c2bf6b2d24c8000ff585c2", catch_response=True) as response:
            if response.json()["_id"] == "58c2bf6b2d24c8000ff585c2":
                response.success()
            else:
                response.failure()


    @task(1)
    def add(self):
        data = {"dataType": "string", "data": "another value"}
        headers = {'content-type': 'application/json'}
        with self.client.post("/api/data", json.dumps(data), \
            headers=headers, catch_response=True) as response:
            if response.json()["_id"] != "":
                response.success()
            else:
                response.failure()

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 1500
