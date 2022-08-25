import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 128, kernel_size=3, stride=1, padding='same')
        self.conv2 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding='same')
        self.conv3 = nn.Conv2d(128, 64, kernel_size=3, stride=1, padding='same')

        self.fc1 = nn.Linear(64*3*3, 243)
        self.fc2 = nn.Linear(3, 3)
        self.fc3 = nn.Linear(3, 9)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        print(x.shape)
        x = F.relu(self.conv2(x))
        print(x.shape)
        x = F.relu(self.conv3(x))
        print(x.shape)
        x = F.relu((self.fc1(x)))
        x = F.relu((self.fc2(x)))
        x = F.softmax(self.fc3(x))

        return x


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

    def train_step(self, state, reward, action, next_state, done):
        self.frame_idx += 1
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
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
