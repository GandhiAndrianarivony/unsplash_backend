import torchvision


class Config:
    def __init__(self):
        pass

    def efficientnet_v2_l(self):
        return torchvision.models.efficientnet_v2_l()
