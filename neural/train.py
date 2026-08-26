import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from neural.model import ConnectFourEvalNet, board_to_tensor
from neural.dataset import load_dataset
class C4Dataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        board, player, label = self.data[idx]
        x = board_to_tensor(board, player)
        y = torch.tensor([label], dtype=torch.float32)
        return x, y

def train(data_path, epochs=20, batch_size=32, lr=1e-3):
    data = load_dataset(data_path)
    dataset = C4Dataset(data)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = ConnectFourEvalNet()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        total_loss = 0.0
        for x, y in loader:
            optimizer.zero_grad()
            pred = model(x)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, loss: {total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "data/model_checkpoint.pt")
    print("Model sacuvan.")
    return model

if __name__ == "__main__":
    train("data/random_games.pkl")