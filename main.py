from environment import autonomous_vehicle
import numpy as np
import torch
from memory_replay import Buffer_replay
from dqn_network import *
from utils import *


class dqn_agent:
    def __init__(self) -> None:
        # Inicializamos el entorno
        self.env = autonomous_vehicle()
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


        # Inicializamos la red neuronal
        self.input_dim = self.env.num_states
        self.output_dim = self.env.num_actions
        self.dqn = DQN(self.input_dim, self.output_dim).to(self.DEVICE)
        self.dqn_target = DQN(self.input_dim, self.output_dim).to(self.DEVICE)
        copy_target(self.dqn_target, self.dqn)

        # Inicializamos el buffer de memoria
        self.buffer = Buffer_replay(1000)

        # Inicializamos los hiperparámetros
        self.epsilon = 0.9
        self.gamma = 0.9
        self.learning_rate = 0.001
        self.batch_size = 128
        self.Timesteps = 5000
        self.optimizer = torch.optim.Adam(self.dqn.parameters(), lr=self.learning_rate)
        self.mejor_reward = -np.inf




    def learn(self):
        state = self.env.reset()
        all_rewards = []
        episode_reward = []
        for t in range(self.Timesteps):
            with torch.no_grad():
                action = self.env.select_action(state)
                next_state, reward, done = self.env.step(action)
                self.buffer.add(state, action, reward, next_state, done)
                state = next_state
                episode_reward.append(reward)
                if done:
                    all_rewards.append(sum(episode_reward))
                    self.guardar_best_model(sum(episode_reward))
                    state = self.env.reset()
                    episode_reward = []

            if len(self.buffer) > self.batch_size:
                loss = self.compute_msbe_loss()
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            
            soft_update(self.dqn_target, self.dqn, 0.01)
            
        
        episode_reward_plot(all_rewards, t, Title='Experience rewards', window_size=5, step_size=1)
            
    def guardar_best_model(self, reward):
        if reward > self.mejor_reward:
            self.mejor_reward = reward
            torch.save(self.dqn_target.state_dict(), 'mejor_modelo.pth')

    def compute_msbe_loss(self):
        device = self.DEVICE
        state_batch, action_batch, reward_batch, next_state_batch, terminated_batch = self.buffer.sample(self.batch_size)

        # Move data to Tensor and also to device to take profit of GPU if available
        state_batch = torch.FloatTensor(state_batch).to(device)
        action_batch = torch.Tensor(action_batch).to(dtype=torch.long).to(device).unsqueeze(1)
        next_state_batch = torch.FloatTensor(next_state_batch).to(device)
        reward_batch = torch.FloatTensor(reward_batch).to(device).unsqueeze(1)
        terminated_batch = torch.FloatTensor(terminated_batch).to(dtype=torch.long).to(device).unsqueeze(1)

        # TODO: Compute the Q-values for the next_state_batch to compute the target
        Q_next = torch.max(self.dqn_target(next_state_batch).detach(),dim=1, keepdim=True)[0]

        # TODO Compute targets. Target for Q(s,a) is standard but when episode terminates target should be only the reward.
        target = reward_batch + self.gamma * Q_next * (1-terminated_batch)

        # TODO Compute the Q-values for the state_batch according to the DQN network
        Q_expected = torch.gather(self.dqn(state_batch), 1, action_batch)

        # TODO Compute the MSE loss between q_expected and target
        criteria = nn.MSELoss()
        loss = criteria(target, Q_expected)
        return loss

                    
                
if __name__ == "__main__":
    dqn = dqn_agent()
    dqn.learn()