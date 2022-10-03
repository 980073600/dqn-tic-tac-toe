import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.input_dim = [3, 3, 3]
        self.output_dim = 9
        self.conv = nn.Sequential(
            nn.Conv2d(self.input_dim[0], 128, kernel_size=3, padding='same'), nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding='same'), nn.ReLU(),
            nn.Conv2d(128, 64, kernel_size=3, padding='same'), nn.ReLU()
        )
        self.fc_input_dim = self.feature_size()
        self.value_stream = nn.Sequential(
            nn.Linear(self.fc_input_dim, 243), nn.ReLU(),
            nn.Linear(243, 1)
        )
        self.advantage_stream = nn.Sequential(
            nn.Linear(self.fc_input_dim, 243), nn.ReLU(),
            nn.Linear(243, self.output_dim)
        )

    def forward(self, x):
        features = self.conv(x)
        features = features.view(features.size(0), -1)
        values = self.value_stream(features)
        advantages = self.advantage_stream(features)
        qvals = values + (advantages - advantages.mean())

        return qvals

    def feature_size(self):
        return self.conv(torch.autograd.Variable(torch.zeros(1, *self.input_dim))).view(1, -1).size(1)

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class Trainer:
    def __init__(self, net, target_net, lr, gamma):
        self.lr = lr
        self.net = net
        self.target_net = target_net
        self.gamma = gamma
        self.beta = 0.00001
        self.optimizer = optim.Adam(net.parameters(), lr=self.lr, weight_decay=self.beta)
        self.loss = nn.MSELoss()
        self.sync_target_frames = 100
        self.frame_idx = 0

    def train_step(self, state, action, reward, next_state, done):
        self.frame_idx += 1
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        next_state = torch.tensor(next_state, dtype=torch.float)
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
                tensor = next_state[idx].view(1, 3, 3, 3)
                next_state_values = self.target_net(tensor)
                q_new = reward[idx] + self.gamma * torch.max(next_state_values)

            target[idx][action] = q_new

        self.optimizer.zero_grad()
        loss = self.loss(target, pred)
        loss.backward()
        self.optimizer.step()

        if self.frame_idx % self.sync_target_frames == 0:
            self.target_net.load_state_dict(self.net.state_dict())
