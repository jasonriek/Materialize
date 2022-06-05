import sys
from PySide6.QtWidgets import (QApplication)

from materialize.window import (Window)

def main():
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    win = Window()
    win.showMaximized()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()



