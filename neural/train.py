import os

import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split

from neural.model import ConnectFourEvalNet, board_to_tensor
from neural.dataset import load_dataset
class C4Dataset(Dataset):
    def __init__(self, data):
        x_list, y_list  = [], []
        for board, player, label in data:
            x_list.append(board_to_tensor(board, player))
            y_list.append(torch.tensor([label], dtype=torch.float32))

        self.x = torch.stack(x_list)
        self.y = torch.stack(y_list)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

def train(data_path=None, model_path=None, plot_path=None, epochs=20, batch_size=128, lr=1e-3, val_ratio=0.2):
    print("---Zapocinjanje treninga---")
    print(f"Dataset: {data_path}")

    data = load_dataset(data_path)
    dataset = C4Dataset(data)
    
    # Podjela na Train i Validation skup
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = ConnectFourEvalNet()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    train_loss_history = []
    val_loss_history = []
    best_val_loss = float("inf")

    for epoch in range(epochs):
        # trening faza
        model.train()
        total_train_loss = 0.0
        for x, y in train_loader:
            optimizer.zero_grad()
            pred = model(x)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)
        train_loss_history.append(avg_train_loss)

        # validaciona faza
        model.eval()
        total_val_loss = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                pred = model(x)
                loss = criterion(pred, y)
                total_val_loss += loss.item()

        avg_val_loss = total_val_loss / len(val_loader)
        val_loss_history.append(avg_val_loss)

        print(f"Epoch {epoch+1}/{epochs}, Train loss: {avg_train_loss:.4f}, Val loss: {avg_val_loss:.4f}")

        # Sačuvano samo ako je val loss poboljšan
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            torch.save(model.state_dict(), model_path)
            print(f"  -> Novi najbolji model sacuvan (val loss: {best_val_loss:.4f})")

    # Cuvanje grafika Loss krive
    os.makedirs("report", exist_ok=True)
    plt.figure()
    plt.plot(range(1, epochs+1), train_loss_history, label="Train Loss")
    plt.plot(range(1, epochs+1), val_loss_history, label="Val Loss", linestyle="--")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title("Trening i Vlidation loss - Connect Four eval mreza")
    plt.savefig(plot_path)
    print(f"Loss kriva sacuvana: {plot_path}")

    return model, train_loss_history, val_loss_history

if __name__ == "__main__":
    # 1. Treniranje - Outcome-based pristup
    '''train(
        data_path="data/dataset_outcome_based.pkl",
        model_path="data/model_checkpoint_v1.pt",
        plot_path="report/loss_curve_v1.png"
    )'''

    # 2. Treniranje - Hibridni pristup
    train(
        data_path="data/dataset_hybrid_10000.pkl",
        model_path="data/model_checkpoint_v2_fin.pt",
        plot_path="report/loss_curve_v2_fin.png"
    )