from locust import HttpUser, task, between

class StressUser(HttpUser):
    # Tiempo de espera entre 1 y 5 segundos entre tareas
    wait_time = between(1, 5)

    @task(1)
    def predict_argentinas(self):
        self.client.post(
            "/predict", 
            json={
                "flights": [
                    {
                        "OPERA": "Aerolineas Argentinas", 
                        "TIPOVUELO": "N", 
                        "MES": 3
                    }
                ]
            }
        )

    @task(1)
    def predict_latam(self):
        self.client.post(
            "/predict", 
            json={
                "flights": [
                    {
                        "OPERA": "Grupo LATAM", 
                        "TIPOVUELO": "N", 
                        "MES": 3
                    }
                ]
            }
        )
