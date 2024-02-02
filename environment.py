from sensor_distancia import Sensor_distancia
from servomotor import ServoMotor
import numpy as np


class autonomous_vehicle:
    def __init__(self, epsilon=0.2, num_actions=4, num_states=1):
        """Environment para entrenar el coche autónomo. Simula como se moveria el coche a través de un sensor de distancia y un servo motor.

        Args:
            epsilon (float, optional): Valor para la técnica de epsilon greedy. Defaults to 0.2.
            num_actions (int, optional): acciones que puede hacer el vehículo. Defaults to 4.
            num_states (int, optional): Estados del vehiculo (distancia_sensor, angulo_servo). Defaults to 1.
        """
        self.sensor = Sensor_distancia()
        self.servo = ServoMotor()
        self.num_actions = 4
        self.num_states = 2
        self.epsilon = 0.9
        self.last_action = 2
        self.traduction = {0: "LEFT", 1: "RIGHT", 2: "UP", 3: "DOWN"}
    
    def reset(self):
        self.sensor = Sensor_distancia()
        self.servo = ServoMotor()
        initial_state = [self.sensor.last_distance, self.servo.angle]
        return initial_state
        
    def step(self, action):
        new_state = [self.sensor.step(), self.servo.step()]
        reward = self.get_reward(new_state, action)
        done = True if new_state[0] < 0.05 else False
        
        print(f"La acción fue {self.traduction[action]} y el estado es {new_state}, se obtuvo una recompensa de {reward}")
        
        return new_state, reward, done
    
    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.num_actions)
        else:
            return self._preprocess_best_action(state)
        
    def get_reward(self, state, action):
        sensor_distance, servo_angle = state[0], state[1]
        if sensor_distance >= 0.45:
            
            return 5 if action != self.last_action else 50
        else:
            if servo_angle <= 45:
                if action == 1:
                    return 50
                else:
                    return -20
                
            elif servo_angle >= 135:
                if action == 0:
                    return 50
                else:
                    return -20
            return -1
        
    def _preprocess_best_action(self, state):
        sensor_distance, servo_angle = state[0], state[1]
        if sensor_distance >= 0.45:
            if servo_angle <= 45:
                self.last_action = 1 # RIGHT
                return 1 # RIGHT
            elif servo_angle >= 135:
                self.last_action = 0
                return 0 # LEFT
            else:
                self.last_action = 2
                return 2 # UP
        else:
            if servo_angle <= 75:
                self.last_action = 1 # RIGHT
                return 1 # RIGHT
            elif servo_angle >= 105:
                self.last_action = 0
                return 0 # LEFT
            else:
                self.last_action = 3
                return 3 # DOWN
        
        
