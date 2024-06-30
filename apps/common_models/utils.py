from pathlib import Path

def upload_to(instance, filename):
    fn = instance.file_name
    ext = Path(filename).suffix
    return f"{fn}{ext}"