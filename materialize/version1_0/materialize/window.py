from PySide6 import (QtWidgets, QtCore)

from materialize.material_table import (MaterialTable)
from materialize.item_tree import (ItemTree)
from materialize.database import (ItemDatabase)
from materialize.search_entry import (SearchEntry)
from materialize.search_table import (SearchTable)

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
        categories = ItemDatabase.categoryNames()
        if categories:
            self.category_combo.addItems(categories)
            self.category_combo.setCurrentText('Parts List')
        else:
            self.category_combo.addItems(['Parts List'])
        
        self.search_entry = SearchEntry(self)
        self.search_entry.returnPressed.connect(self.search)
        self.search_table = SearchTable(self)
        self.search_table.itemDoubleClicked.connect(self.addItem)

        self.material_table = MaterialTable(self)

        self.setupLayout()
    
    def addItem(self, item:QtWidgets.QTreeWidgetItem, colunmn:int):
        item_text = item.text(0)
        category = item.text(1).split('/')[-2]
        notes = ItemDatabase.notes(category, item_text)
        item_row = self.material_table.itemAtRow(item_text)
        if item_row == -1:   
            self.material_table.addItem(1, item_text, category, notes)
        else:
            self.material_table.cellWidget(item_row, self.material_table.QUANTITY_COL).inc()

    def search(self):
        search_key = self.search_entry.text().strip()
        category_text = self.category_combo.currentText()
        if search_key:
            self.search_table.setSearchResults(self.search_entry.itemPathsFromTree(search_key, self.tree))
        else: 
            self.search_table.clearTable()

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
        self.top_layout.addWidget(self.search_entry)
        self.top_layout.addWidget(self.category_combo)
        self.main_layout.addWidget(self.top_area)
        self.main_layout.addWidget(self.search_table)
        self.main_layout.addWidget(self.material_table)

        self.setCentralWidget(self.main_widget)

