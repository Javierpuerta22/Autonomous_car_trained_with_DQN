import serial
import time
import torch
from dqn_network import DQN

dqn = DQN(2, 4)
dqn.load_state_dict(torch.load("mejor_modelo.pth"))
dqn.eval()
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

while True:
    #Leemos la lectura del sensor y el angulo del servomotor y la enviamos a la red neuronal
    state = arduino.readline().decode('utf-8').split()
    servo_angle = int(state[1])
    sensor_distance = float(state[0])
    state = torch.tensor([sensor_distance, servo_angle], dtype=torch.float32)
    resultado = dqn(state)
    
    #hacemos el argmax para obtener la acción y la enviamos al arduino
    accion = torch.argmax(resultado).item()
    arduino.write(f"{accion}\n".encode('utf-8'))