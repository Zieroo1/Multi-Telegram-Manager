from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
                             QLabel, QFrame, QCheckBox)
from PyQt5.QtCore import Qt, QPoint
from drag_and_drop_widget import drag_and_drop_widget
from action import view_model
from style import title_label_style, profile_list_style, button_style_style, button_close_style, button_main_style, checkbox_style


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
        self.title_label.setStyleSheet(title_label_style)
        self.title_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(self.title_bar)
        header_layout.addSpacing(10)  # Left spacer
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        # Window control buttons
        self.minimize_button = QPushButton('--')
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet(button_main_style("#383838"))

        self.fullscreen_button = QPushButton('[  ]')
        self.fullscreen_button.setFixedSize(30, 30)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_button.setStyleSheet(button_main_style("#383838"))

        self.close_button = QPushButton('X')
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet(button_close_style("#383838"))

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
        self.view_model.data_changed.connect(self.update)
        self.update()

        self.profile_list.setStyleSheet(profile_list_style)

        self.profile_list.itemClicked.connect(self.view_model.on_item_clicked)

        content_layout.addWidget(self.profile_list)

        buttons_dragdrop_layout = QVBoxLayout()

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.async_launch)
        self.stop_button = QPushButton('Kill all TG\'s')
        self.stop_button.clicked.connect(self.view_model.stop)
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.view_model.delete_profile)
        self.select_all_button = QPushButton('Select All')
        self.select_all_button.clicked.connect(self.view_model.select_all_action)
        self.unselect_all_button = QPushButton('Unselect All')
        self.unselect_all_button.clicked.connect(self.view_model.unselect_all_action)
        self.scale = QCheckBox('Scale TG\'s')
        self.scale.clicked.connect(self.view_model.switch_scale)
        self.scale.setStyleSheet(checkbox_style)

        self.start_button.setStyleSheet(button_style_style)
        self.stop_button.setStyleSheet(button_style_style)
        self.delete_button.setStyleSheet(button_style_style)
        self.select_all_button.setStyleSheet(button_style_style)
        self.unselect_all_button.setStyleSheet(button_style_style)

        buttons_dragdrop_layout.addWidget(self.start_button)
        buttons_dragdrop_layout.addWidget(self.stop_button)
        buttons_dragdrop_layout.addWidget(self.delete_button)
        buttons_dragdrop_layout.addWidget(self.select_all_button)
        buttons_dragdrop_layout.addWidget(self.unselect_all_button)
        buttons_dragdrop_layout.addWidget(self.scale)

        self.drag_drop_widget = drag_and_drop_widget()
        buttons_dragdrop_layout.addWidget(self.drag_drop_widget)
        self.drag_drop_widget.files_added.connect(self.view_model.update)

        content_layout.addLayout(buttons_dragdrop_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

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

    def update(self):
        self.profile_list.clear()
        for i in self.view_model.profile_items:
            self.profile_list.addItem(i)

    def async_launch(self):
        self.view_model.start_worker(self.view_model.launch)