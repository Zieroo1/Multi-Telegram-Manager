import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap

def get_tguncli():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_icon_path = os.path.join(script_dir, 'tguncli.png')
    return QPixmap(absolute_icon_path).scaled(QSize(38, 38))

def get_tgcli():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_icon_path = os.path.join(script_dir, 'tgcli.png')
    return QPixmap(absolute_icon_path).scaled(QSize(38, 38))