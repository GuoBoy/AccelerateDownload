import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow,run

def test():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # test()
    run()