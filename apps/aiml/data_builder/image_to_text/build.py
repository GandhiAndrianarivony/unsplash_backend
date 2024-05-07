from PIL import Image
import joblib

import environ

env = environ.Env()

def build_image_to_text_model_data_processor():
    return joblib.load(env("IMAGE_TO_TEXT_PROCESSOR"))