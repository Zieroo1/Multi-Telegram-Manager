from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem
from model.profile import profile
from resourses.resource import get_resource


class image_list_item(QListWidgetItem):
    def __init__(self, profile_name, parent=None):
        super(image_list_item, self).__init__(parent)
        self.unchecked_icon = QIcon(get_resource('gui_img/tguncli.png'))
        self.checked_icon = QIcon(get_resource('gui_img/tgcli.png'))
        self.setIcon(self.unchecked_icon)
        self.item = profile(profile_name)
        self.setText(f'Profile {self.item.name}')

    def setChecked(self, checked):
        if checked:
            self.setIcon(self.checked_icon)
            self.item.select = True
        else:
            self.setIcon(self.unchecked_icon)
            self.item.select = False