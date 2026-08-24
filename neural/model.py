"""
MLP arhitektura za evaluaciju stanja Connect Four table

Input: 42 polja (6x7 tabla), enkodirano kao {-1, 0, 1}
    -1 = protivnik, 0 = prazno, 1 = moja figura

Output: skalar u [-1, 1] (tanh)
"""

import torch
import torch.nn as nn

class ConnectFourEvalNet(nn.Module):
    def __init__(self, input_size=42, hidden1=64, hidden2=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden1),
            nn.ReLU(),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Linear(hidden2, 1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.net(x)

# Funkcija za konvertovanje board reprezentacije u tensor za nn
def board_to_tensor(board, player):
    flat = []
    for cell in board:
        if cell  == 0:
            flat.append(0.0)
        elif cell == player:
            flat.append(1.0)
        else:
            flat.append(-1.0)
    return torch.tensor(flat, dtype=torch.float32)

if __name__ == "__main__":
    model = ConnectFourEvalNet()
    x = torch.zeros(42)
    output = model(x)
    print(f"Model OK, output shape:", output.shape, "value:", output.item())