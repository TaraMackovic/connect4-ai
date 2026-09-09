"""
CNN arhitektura za evaluaciju stanja Connect Four table

Input: Tenzor oblika (2, 6, 7) sa 2 binarna kanala
Output: skalar u [-1, 1] (tanh)

"""
from game.board import ROWS, COLS

import torch
import torch.nn as nn

class ConnectFourEvalNet(nn.Module):
    def __init__(self, conv1_channels=32, conv2_channels=64):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(2, conv1_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(conv1_channels, conv2_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Flatten()
        )
        self.fc = nn.Sequential(
            nn.Linear(conv2_channels * ROWS * COLS, conv2_channels),
            nn.ReLU(),
            nn.Linear(conv2_channels, 1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.fc(self.conv(x))
    
# Funkcija za konvertovanje board reprezentacije u tensor za nn
def board_to_tensor(board, player):
    my_tokens = [[1.0 if cell == player else 0.0 for cell in row] for row in board]
    opp_player = 2 if player == 1 else 1
    opp_tokens = [[1.0 if cell == opp_player else 0.0 for cell in row] for row in board]

    return torch.tensor([my_tokens, opp_tokens], dtype=torch.float32)

if __name__ == "__main__":
    model = ConnectFourEvalNet()
    x = torch.zeros(1, 2, ROWS, COLS) # batch = 1, kanala = 2
    output = model(x)
    print(f"Model OK, output shape:", output.shape, "value:", output.item())