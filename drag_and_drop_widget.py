import os
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class drag_and_drop_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        self.label = QLabel("Перетащите файлы сюда", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-family: Poppins;
            }
        """)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addStretch()

        self.setStyleSheet("""
            DragDropWidget {
                background-color: #383838;
                border: 2px solid #2D2D2D;
                border-radius: 10px;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        tdatas_folder = 'tdatas'
        if not os.path.exists(tdatas_folder):
            os.makedirs(tdatas_folder)

        for url in urls:
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                base_name, ext = os.path.splitext(os.path.basename(file_path))
                new_file_name = self.get_new_filename(os.path.join(tdatas_folder, base_name), ext)
                new_file_path = os.path.join(tdatas_folder, new_file_name)
                shutil.copy(file_path, new_file_path)

        self.label.setText("Файлы успешно добавлены")

    def dragLeaveEvent(self, event):
        event.accept()

    def get_new_filename(self, base_path, ext):
        i = 0
        while os.path.exists(f"{base_path}_{i}{ext}"):
            i += 1
        return f"{os.path.basename(base_path)}_{i}{ext}"