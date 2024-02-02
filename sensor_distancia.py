from sklearn.preprocessing import MinMaxScaler
import numpy as np



class Sensor_distancia:
    def __init__(self):
        self.last_distance = 0.5
        
    def step(self):
        ruido_gaussiano = np.random.normal(0, 0.2, 1)
        self.last_distance = np.clip(self.last_distance + ruido_gaussiano, 0, 1)
        
        return self.last_distance[0]
