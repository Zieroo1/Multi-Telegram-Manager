import os
import subprocess
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
                             QLabel, QFrame)
from PyQt5.QtCore import Qt, QSize, QPoint


from drag_and_drop_widget import drag_and_drop_widget
from image_list_item import image_list_item
from action import view_model


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('TG Starter')
        self.setGeometry(100, 100, 1280, 720)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Custom title bar
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(30)
        self.title_bar.setStyleSheet("background-color: #484848; border-radius: 10px;")
        header_layout.addWidget(self.title_bar)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(30, 0, 0, 0)  # Add left margin to move text from the edge
        title_layout.addStretch()

        # Title text
        self.title_label = QLabel("TG Starter")
        self.title_label.setStyleSheet("""
                   QLabel {
                       color: #FFFFFF;
                       font-size: 16px;
                       font-family: Poppins;
                       font-size: 20px;
                       font-weight: bold;
                   }
               """)
        self.title_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(self.title_bar)
        header_layout.addSpacing(10)  # Left spacer
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        # Window control buttons
        self.minimize_button = QPushButton('--')
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet(self.button_style("#383838"))

        self.fullscreen_button = QPushButton('[  ]')
        self.fullscreen_button.setFixedSize(30, 30)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_button.setStyleSheet(self.button_style("#383838"))

        self.close_button = QPushButton('X')
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet(self.button_style_close("#383838"))

        header_layout.addWidget(self.minimize_button)
        header_layout.addWidget(self.fullscreen_button)
        header_layout.addWidget(self.close_button)

        self.isPressed = False
        self.startPos = QPoint()

        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.setStyleSheet("background-color: #484848; border-radius: 10px;")

        self.profile_list = QListWidget()
        self.profile_list.setSelectionMode(QListWidget.MultiSelection)

        self.view_model = view_model('tdatas')

        for i in self.view_model.profile_items:
            self.profile_list.addItem(i)

        self.profile_list.setStyleSheet("""
            QListWidget {
                background-color: #383838;
                border: 2px solid #2D2D2D;
            }
            QListWidget::item {
                color: #FFFFFF;
                background-color: #484848;
                padding: 5px;
                border: 1px solid #2D2D2D;
                width: 180px;
                height: 43px;
                border-radius: 10px;
                font-size: 20px;
                font-family: Poppins;
                font-weight: medium;
            }
            QListWidget::item:selected {
                background-color: #717171;
            }
            QListWidget::item:selected:!active {
                background-color: #484848;
            }
            QListWidget::item:selected:active {
                background-color: #717171;
            }
        """)

        self.profile_list.itemClicked.connect(self.view_model.on_item_clicked)

        content_layout.addWidget(self.profile_list)

        buttons_dragdrop_layout = QVBoxLayout()

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.view_model.launch)
        self.stop_button = QPushButton('Stop')
        self.delete_button = QPushButton('Delete')
        self.select_all_button = QPushButton('Select All')
        self.select_all_button.clicked.connect(self.view_model.select_all_action)
        self.unselect_all_button = QPushButton('Unselect All')
        self.unselect_all_button.clicked.connect(self.view_model.unselect_all_action)

        button_style = """
            QPushButton {
                background-color: #383838;
                color: white;
                border-radius: 10px;
                font-size: 28px;
                font-family: Poppins;
                font-weight: medium;
                padding: 10px;
                min-width: 245px;
                min-height: 59px;
                border: 2px solid #2D2D2D;
            }
            QPushButton:hover {
                background-color: #717171;
            }
        """
        self.start_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.select_all_button.setStyleSheet(button_style)
        self.unselect_all_button.setStyleSheet(button_style)

        buttons_dragdrop_layout.addWidget(self.start_button)
        buttons_dragdrop_layout.addWidget(self.stop_button)
        buttons_dragdrop_layout.addWidget(self.delete_button)
        buttons_dragdrop_layout.addWidget(self.select_all_button)
        buttons_dragdrop_layout.addWidget(self.unselect_all_button)

        self.drag_drop_widget = drag_and_drop_widget()
        buttons_dragdrop_layout.addWidget(self.drag_drop_widget)

        content_layout.addLayout(buttons_dragdrop_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def button_style(self, bg_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: 1px solid #2D2D2D;
                font-family: Poppins;
                font-weight: bold;
                border-radius: 10px;
                min-width: 47px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: #717171;
            }}
        """
    def button_style_close(self, bg_color):
        return f"""
            QPushButton {{
                background-color: #661717;
                color: white;
                border: 1px solid #2D2D2D;
                font-family: Poppins;
                font-weight: bold;
                border-radius: 10px;
                min-width: 47px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: #A92525;
            }}
        """

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isPressed = True
            self.startPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.isPressed:
            self.move(event.globalPos() - self.startPos)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
