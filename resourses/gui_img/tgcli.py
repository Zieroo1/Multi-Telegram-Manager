from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap

def get_tguncli():
    return QPixmap('tguncli.png').scaled(QSize(38, 38))

def get_tgcli():
    return QPixmap('tgcli.png').scaled(QSize(38, 38))