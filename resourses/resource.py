import os

def get_resource(resource_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_icon_path = os.path.join(script_dir, resource_name)
    return absolute_icon_path