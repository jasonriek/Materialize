from PySide6 import (QtWidgets)

from materialize.material_table import (MaterialTable)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Materialize')
        
        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        self.material_table = MaterialTable(self)
        self.material_table.addItem(2, 'Open front seats')
        self.material_table.addItem(2, 'Screws')
        self.material_table.addItem(5, 'Pipes')
        self.material_table.addItem(3, 'Nuts')

        self.setupLayout()

    def setupLayout(self):
        self.main_layout.addWidget(self.material_table)

        self.setCentralWidget(self.main_widget)

