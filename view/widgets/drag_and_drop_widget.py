import os
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from resourses import drag_and_drop_style
from model.worker import worker


class drag_and_drop_widget(QWidget):
    files_added = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        self.label = QLabel("Drop your tdata's here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(drag_and_drop_style)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addStretch()

        self.setLayout(layout)  # Устанавливаем макет для виджета

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            print("dragEnterEvent: URLs detected")
        else:
            print("dragEnterEvent: No URLs detected")

    def dropEvent(self, event):
        self.worker = worker(self.copy_profile,event.mimeData().urls())
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def dragLeaveEvent(self, event):
        event.accept()
        print("dragLeaveEvent")

    def copy_directory(self, dir_path, tdatas_folder):
        base_name = os.path.basename(dir_path)
        new_dir_name = self.get_new_dirname(os.path.join(tdatas_folder, base_name))
        new_dir_path = os.path.join(tdatas_folder, new_dir_name)
        shutil.copytree(dir_path, new_dir_path)
        print(f"Скопирована папка: {dir_path} в {new_dir_path}")

    def get_new_dirname(self, base_path):
        i = 0
        while os.path.exists(f"{base_path}_{i}"):
            i += 1
        new_dir_name = f"{os.path.basename(base_path)}_{i}"
        print(f"Новое имя папки: {new_dir_name}")
        return new_dir_name

    def copy_profile(self, urls):
        print(f"dropEvent: {len(urls)} items detected")
        tdatas_folder = 'tdatas'
        if not os.path.exists(tdatas_folder):
            os.makedirs(tdatas_folder)
            print(f"Создана папка: {tdatas_folder}")

        for url in urls:
            file_path = url.toLocalFile()
            print(f"Обработка пути: {file_path}")
            if os.path.isdir(file_path) and os.path.basename(file_path) == 'tdata':
                self.copy_directory(file_path, tdatas_folder)
            else:
                print(f"Игнорируется: {file_path} (не папка или не 'tdata')")

        self.files_added.emit()
