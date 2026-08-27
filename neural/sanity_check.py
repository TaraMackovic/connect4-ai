import torch
from neural.model import ConnectFourEvalNet, board_to_tensor

def sanity_check():
    model = ConnectFourEvalNet()
    model.load_state_dict(torch.load("data/model_checkpoint.pt"))
    model.eval()

    # skoro-pobjeda za igraca 1

    board_near_win = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
    ]

    with torch.no_grad():
        x = board_to_tensor(board_near_win, player=1)
        score = model(x).item()
        print(f"Skoro-pobjeda za igraca 1, ocjena za igraca 1: {score:.4f}")

        x_opp = board_to_tensor(board_near_win, player=2)
        score_opp = model(x_opp).item()
        print(f"Ista pozicija, ocjena za igraca 2: {score_opp:.4f}")

if __name__ == "__main__":
    sanity_check()