from PySide6 import (QtWidgets)

class SearchTable(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setColumnCount(2)
        self.setHeaderLabels(['Item', 'Path'])
        self.setMaximumHeight(100)

    def clearTable(self):
        self.clear()
        self.setColumnCount(2)
        self.setHeaderLabels(['Item', 'Path'])

    def setSearchResults(self, data:list):
        items = []
        self.clearTable()
        if data:           
            for row in data:
                item = QtWidgets.QTreeWidgetItem(row)
                items.append(item)
            self.addTopLevelItems(items)
