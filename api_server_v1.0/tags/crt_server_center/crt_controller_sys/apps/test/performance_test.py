from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def update_state_api(self):
        # data = {
        #     "ctrl_no": 1,
        #     "ctrl_type": 1,
        #     "ctrl_state": 0,
        #     "evt_num": 0,
        #     "alarm_evt_num": 0,
        #     "fault_evt_num": 0,
        #     "feedback_evt_num": 0,
        #     "action_evt_num": 0,
        #     "supervisor_evt_num": 0,
        #     "shielding_evt_num": 0,
        #     "operate_evt_num": 0,
        #     "vl_action_evt_num": 0,
        #     "vl_fault_evt_num": 0,
        #     "vl_shielding_evt_num": 0
        # }
        # self.client.post("/api/v1_0/new/update_state_api", json=data)
        self.client.get("/")
