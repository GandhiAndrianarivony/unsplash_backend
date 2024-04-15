import os

import torch.nn as nn
import torch
from apps.aiml.configs.default import Config


class PreTrainModel(nn.Module):
    def __init__(self, model_name: str):
        super().__init__()

        self.architecture = os.path.splitext(os.path.basename(model_name))[0]
        self.model = self._load_model()
        self._load_state_dict(model_name)

    def forward(self, x):
        return self.model(x)

    def _load_model(self):
        config = Config()
        return getattr(config, self.architecture)()
    
    def _load_state_dict(self, model_name):
        self.model.load_state_dict(torch.load(model_name))
