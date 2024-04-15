import environ

import joblib


env = environ.Env()


def build_transform():
    return joblib.load(env("TRANSFORM"))

def build_categories():
    return joblib.load(env("CATEGORIES"))