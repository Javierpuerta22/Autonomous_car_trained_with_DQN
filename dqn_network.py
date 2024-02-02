# Description: This file contains the DQN network architecture.
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
def copy_target(target, source):
    """Copies the parameters from the source network to the target network.
    Args:
     -target (nn.Module): The target network to copy the parameters to.
     -source (nn.Module): The source network to copy the parameters from.
    """
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(param.data)

def soft_update(target_model, local_model,tau):
    """
    The function performs a soft update of the target model's parameters using the local model's
    parameters and a given tau value.
    Args:
     - target_model (nn.Module) : The target_model is the model that we want to update gradually towards the
    local_model
     - local_model (nn.Module): The local_model is the model whose parameters we want to update. It is the model
    that we want to use to update the target_model
     - tau (float): The parameter "tau" is a value between 0 and 1 that determines the weight given to the
    local model's parameters when updating the target model's parameters. A higher value of tau gives
    more weight to the local model's parameters, while a lower value gives more weight to the target
    model's
    """
    for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
          target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)