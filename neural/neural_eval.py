import torch
from neural.model import ConnectFourEvalNet, board_to_tensor

MODEL_PATH = "data/model_checkpoint_v2.pt"

_model = None

def _load_model():
    global _model
    if _model is None:
        model = ConnectFourEvalNet()
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()
        _model = model
    return _model

def evaluate(board, player):
    model = _load_model()
    with torch.no_grad():
        x = board_to_tensor(board, player)
        x = x.unsqueeze(0) # pretvara u batch oblik
        score = model(x).item()
    return score