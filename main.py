import sys

from PyQt5.QtWidgets import QApplication
from view.windows.gui_app import MyApp


def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
