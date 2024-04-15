from PIL import Image

from .transforms.build import build_transform, build_categories

def build_data(image: Image):
    transform = build_transform()
    categories = build_categories()
    return transform(image).unsqueeze(dim=0), categories