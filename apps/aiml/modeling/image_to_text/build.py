import os

import torch.nn as nn

from apps.aiml.configs.default import Config


class ImageToTextModel(nn.Module):
    def __init__(self, model_weight):
        super().__init__()

        self.model_weight = model_weight
        self.architecture = os.path.splitext(os.path.basename(model_weight))[0]
        self.model = self._load_model()
        print(f"[INFO] Architecture: {self.architecture}")

    def forward(self, x):
        return self.model.generate(x)

    def _load_model(self):
        config = Config(vit_gpt2_weights=self.model_weight)
        return getattr(config, self.architecture)()
