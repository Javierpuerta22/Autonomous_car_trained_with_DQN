import random
import numpy as np
from collections import deque

class Buffer_replay:
    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)
        self.buffer_size = buffer_size

    def add(self, state, action, reward, next_state, done):
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        batch = random.sample(self.buffer, min(len(self.buffer),batch_size))
        state, action, reward, next_state, terminated = map(np.stack, zip(*batch))
        return state, action, reward, next_state, terminated

    def __len__(self):
        return len(self.buffer)