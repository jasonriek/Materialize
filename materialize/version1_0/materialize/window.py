from PySide6 import (QtWidgets, QtCore)

from materialize.material_table import (MaterialTable)
from materialize.item_tree import (ItemTree)
from materialize.database import (ItemDatabase)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Materialize')
        self.setupItemTree()

        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.top_area = QtWidgets.QGroupBox('Search', self)
        self.top_layout = QtWidgets.QHBoxLayout(self.top_area)
        self.category_combo = QtWidgets.QComboBox(self)
        self.category_combo.addItems(ItemDatabase.categories())

        self.material_table = MaterialTable(self)
        self.material_table.addItem(2, 'Open front seats')
        self.material_table.addItem(2, 'Screws')
        self.material_table.addItem(5, 'Pipes')
        self.material_table.addItem(3, 'Nuts')

        self.setupLayout()
    
    def setupItemTree(self):
        self.tree = ItemTree(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('Select a Category to Search From:')
        item = self.tree.loadItems()
        self.tree.addTopLevelItem(item)
        self.tree_dock = QtWidgets.QDockWidget('Parts List', self)
        self.tree_dock.setWidget(self.tree)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.tree_dock)

    def setupLayout(self):
        self.top_layout.addWidget(self.category_combo)
        self.main_layout.addWidget(self.top_area)
        self.main_layout.addWidget(self.material_table)

        self.setCentralWidget(self.main_widget)

