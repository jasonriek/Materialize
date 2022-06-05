from PySide6 import QtWidgets
from PySide6.QtCore import (Qt, Slot)

from materialize.database import (ItemDatabase)

class SearchEntry(QtWidgets.QLineEdit):
    def __init__(self, *args):
        super().__init__(*args)

    def setNewCompleter(self, items:list):
        completer = QtWidgets.QCompleter(items,self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(completer)
    
    def itemPathsFromTree(self, search_key:str, tree:QtWidgets.QTreeWidget):
        self.items = []
        self.iterItems(self.items, tree.invisibleRootItem())
        item_paths = [[item.text(0), self.itemPath(item)] for item in self.items if search_key.lower() in item.text(0).lower() and item.text(0) != 'Parts List']
        self.items.clear()
        return item_paths

    def iterItems(self, items:list, item:QtWidgets.QTreeWidgetItem):
        items.append(item)
        child_count = item.childCount()
        if child_count:
            for i in range(child_count):
                child = item.child(i)
                self.iterItems(items, child)
                
    def itemPath(self, item:QtWidgets.QTreeWidgetItem):
        item_name = item.text(0)
        parents = []
        next_parent = item.parent()
        while next_parent:
            parents.insert(0, next_parent.text(0))
            next_parent = next_parent.parent()
        parents.append(item_name)

        item_path = '/'.join(parents)
        return item_path
    
    @Slot(str, QtWidgets.QTreeWidget)
    def loadFromTree(self, search_key:str, tree:QtWidgets.QTreeWidget):
        item_paths = self.setItemPathsFromTree(search_key, tree)
  
    
    @Slot(str)
    def reloadItems(self, category_name):
        items = []
        if category_name == 'Parts List':
            categories = ItemDatabase.categoryNames()        
            for cat in categories:
                items.extend(ItemDatabase.items(cat))
        else:
            items = ItemDatabase.items(category_name)
        self.setNewCompleter(items)

            
        

