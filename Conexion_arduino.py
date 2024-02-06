import serial
import time
import torch
from dqn_network import DQN

dqn = DQN(2, 4)
dqn.load_state_dict(torch.load("mejor_modelo.pth", map_location=torch.device('cpu')))
dqn.eval()


#función para obtener un valor entre 0 y 1 en valores que van entre 30 y 5
def map_values(value):
    if value > 30:
        return 1
    elif value < 5:
        return 0
    else:
        return (value -5) / (30 -5)
    
traduction = {0: "LEFT", 1: "RIGHT", 2: "UP", 3: "DOWN"}

try:
    arduino = serial.Serial("COM4", 9600, timeout=1)
    time.sleep(1)

    while True:
        #Leemos la lectura del sensor y el angulo del servomotor y la enviamos a la red neuronal
        
        data= arduino.readline().decode("ascii").strip().split(",")
        if len(data) != 2 or data[0] == "" or data[1] == "":
            continue
        #transformamos la lista con los datos a float y la pasamos a tensor
        data = torch.tensor([map_values(float(data[0])), float(data[1])])
        #obtenemos la acción que la red neuronal considera la mejor
        action = dqn(data).argmax().item()
        #enviamos la acción al arduino
        arduino.write(str(action).encode())
        print("Respuesta del Arduino:", data, "y la acción fue:", traduction[action])
        
    
except Exception as e:
    print(e)
    arduino.close()
    print("Connection closed")
    
finally:
    arduino.close()
    print("Connection closed")