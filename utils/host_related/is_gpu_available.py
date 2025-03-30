import torch

def USE_GPU():
    return torch.cuda.is_available()