import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding='same'), nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding='same'), nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding='same'), nn.ReLU()
        )
        self.flat = nn.Flatten(-3, -1)
        self.value_stream = nn.Sequential(
            nn.Linear(2304, 243), nn.ReLU(),
            nn.Linear(243, 1)
        )
        self.advantage_stream = nn.Sequential(
            nn.Linear(2304, 243), nn.ReLU(),
            nn.Linear(243, 9)
        )

    def forward(self, x):
        features = self.conv(x)
        features = self.flat(-3, -1)
        #features = features.view(features.size(0), -1)
        values = self.value_stream(features)
        advantages = self.advantage_stream(features)
        qvals = values + (advantages - advantages.mean())

        return qvals


class Trainer:
    def __init__(self, net, target_net, lr, gamma):
        self.lr = lr
        self.net = net
        self.target_net = target_net
        self.gamma = gamma
        self.optimizer = optim.Adam(net.parameters(), lr=self.lr)
        self.loss = nn.MSELoss()
        self.sync_target_frames = 100
        self.frame_idx = 0

    def train_step(self, state, action, reward, next_state, done):
        self.frame_idx += 1
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        if len(state.shape) == 3:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.net(state)

        target = pred.clone()
        for idx in range(len(done)):

            q_new = reward[idx]

            if not done[idx]:
                next_state_values = self.target_net(next_state[idx])
                q_new = reward[idx] + self.gamma * torch.max(next_state_values)

            target[idx][torch.argmax(action).item()] = q_new

        self.optimizer.zero_grad()
        loss = self.loss(target, pred)
        loss.backward()
        self.optimizer.step()

        if self.frame_idx % self.sync_target_frames == 0:
            self.target_net.load_state_dict(self.net.state_dict())
