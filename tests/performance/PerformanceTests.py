from locust import task, HttpUser, between


class PerformanceTests(HttpUser):
    wait_time = between(0.5, 2)

    def on_start(self):
        response = self.client.post("/ai/security/login", {
             "username": "test",
             "password": "test"
        })

    # Security Services
    @task(1)
    def security_login(self):
        self.client.post("/ai/security/login", {
            "username": "test",
            "password": "test"
        })

    # AI Services
    """
    @task(1)
    def ai_trainmodel(self):
        self.client.post("/ai/trainmodel", {
            "class_name": "ai.aimodels.GeneralPatientPredictionAIModel.GeneralPatientPredictionAIModel",
            "dataset_parameters" : {
                "dataset_start_time": "01.01.2019",
                "dataset_end_time": "01.12.2021",
                "window_size": 3,
                "test_ratio": 0.2
            },
            "hyperparameters" : {
                "parameters":{
                    "batch_size": [8],
                    "nb_epoch": [5],
                    "optimizer": ["adam"],
                    "activation": ["tanh"],
                    "init_mode": ["normal"],
                    "dropout_rate": [0.4],
                    "units": [150]
                }

            }
        }
        )
    
    @task(1)
    def ai_activatemodel(self):
        self.client.put("/ai/activatemodel", {
            "class_name": "ai.aimodels.GeneralPatientPredictionAIModel.GeneralPatientPredictionAIModel",
            "version": 2
        })
    """

    # @task(1)
    # def ai_prediction(self):
    #     self.client.post("/ai/prediction", {
    #     "ai_model_class": "ai.aimodels.GeneralPatientPredictionAIModel.GeneralPatientPredictionAIModel",
    #     "reference_table": "BloodPressure, HemsireGozlem",
    #     "reference_id": 3004367615,
    #     "prediction_date": "01.01.2017",
    #     "prediction_input": {
    #         "prediction_input": [[-50.0, 36.8, 90, 144, 88, 97, 0, 0, 0, 0], [-70.0, 36.6, 89, 124, 80, 98, 0, 0, 0, 0], [-30.0, 36.5, 82, 121, 83, 97, 0, 0, 0, 0]]
    #     }
    # })

    @task(1)
    def get_ai_prediction(self):
        self.client.get("/ai/prediction/1")

    @task(1)
    def get_ai_notification(self):
        self.client.get("/ai/notification/1")

    @task(1)
    def ai_notification_list(self):
        self.client.get("/ai/notification/list")

    @task(1)
    def ai_statistics(self):
        self.client.post("/ai/statistics", {
            "start_date": "01.01.2018",
            "end_date": "01.01.2020"
        })
