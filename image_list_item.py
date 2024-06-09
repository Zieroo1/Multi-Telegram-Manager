from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QListWidgetItem

from profile import profile


class image_list_item(QListWidgetItem):
    def __init__(self, unchecked_icon_path, checked_icon_path, text, icon_size, profile_name, parent=None):
        super(image_list_item, self).__init__(parent)
        unchecked_pixmap = QPixmap(unchecked_icon_path).scaled(icon_size)
        checked_pixmap = QPixmap(checked_icon_path).scaled(icon_size)
        self.unchecked_icon = QIcon(unchecked_pixmap)
        self.checked_icon = QIcon(checked_pixmap)
        self.setIcon(self.unchecked_icon)
        self.setText(text)
        self.item = profile(text, profile_name)

    def setChecked(self, checked):
        if checked:
            self.setIcon(self.checked_icon)
            self.item.select = True
        else:
            self.setIcon(self.unchecked_icon)
            self.item.select = False