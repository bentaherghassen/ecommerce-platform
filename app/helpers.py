import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app

def save_picture(form_picture, path, output_size=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, path, picture_name)
# Ensure the directory exists
    directory = os.path.dirname(picture_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    i = Image.open(form_picture)
    if output_size:
        i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

def delete_picture(image_path):
    try:
        os.remove(image_path)
    except FileNotFoundError:
        # Handle the case where the file doesn't exist (optional)
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"Error deleting image: {e}")
