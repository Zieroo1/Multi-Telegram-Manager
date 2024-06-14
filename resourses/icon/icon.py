import base64
import os

def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def get_icon():
    icon_path = "icon25.png"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_icon_path = os.path.join(script_dir, icon_path)
    return image_to_base64(absolute_icon_path)