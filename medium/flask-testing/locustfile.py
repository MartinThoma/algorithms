# Third party modules
from locust import HttpUser, between, task


class MyWebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def load_main(self):
        self.client.get("/")
