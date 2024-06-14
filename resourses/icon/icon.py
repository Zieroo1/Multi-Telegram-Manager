import os

def get_icon():
    icon_path = "icon25.png"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_icon_path = os.path.join(script_dir, icon_path)
    return absolute_icon_path