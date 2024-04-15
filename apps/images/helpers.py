from PIL import Image as pil_image
from pathlib import Path

import blurhash

def generate_blurhash_code(image):
    image = pil_image.open(image)
    return blurhash.encode(image, x_components=4, y_components=3)


def save_uploaded_file(uploaded_file, dest):
    """Fuction being used to write on local"""
    # Save the file to the server
    dest_dir = Path(dest)
    dest_dir.mkdir(parents=True, exist_ok=True)

    with open(f"{dest}/" + uploaded_file.name, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return f"{dest}/{uploaded_file.name}"