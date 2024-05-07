import torchvision
from transformers import VisionEncoderDecoderModel


class Config:
    def __init__(self, vit_gpt2_weights=None):
        self.vit_gpt2_weights = vit_gpt2_weights

    def efficientnet_v2_l(self):
        return torchvision.models.efficientnet_v2_l()

    def vit_gpt2_image_captioning(self):
        if self.vit_gpt2_weights is not None:
            return VisionEncoderDecoderModel.from_pretrained(self.vit_gpt2_weights)
        else:
            raise ValueError("Missing weight")