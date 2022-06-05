import os
import sys
import json
import traceback
from unicodedata import category 
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem)
from PySide6.QtCore import (Qt, QPoint)
from PySide6.QtGui import (QAction)

from database import ItemDatabase

class ItemTree(QTreeWidget):
    JSON_PATH = 'db/categories.json'
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.root_item = QTreeWidgetItem(['Parts List'])
        #self.itemDoubleClicked.connect(self.showItem)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
    
    def showContextMenu(self, position:QPoint):
        item = self.itemAt(position)
        if not item:
            return 
        menu = QtWidgets.QMenu(self)
        show_item_action = QAction('Show Item Text', self)
        show_item_action.triggered.connect(self.showItem(item))
        add_sub_cat_action = QAction('Add Sub-Item', self)
        add_sub_cat_action.triggered.connect(self.addSubItem(item))
        menu.addAction(show_item_action)
        menu.addSeparator()
        menu.addAction(add_sub_cat_action)
        menu.exec(self.viewport().mapToGlobal(position))

    
    def showItem(self, item):
        def _showItem():
            print(item.text(0))
        return _showItem

    def addSubItem(self, item:QTreeWidgetItem):
        def _addSubItem():
            text, ok = QtWidgets.QInputDialog.getText(self, f'Sub-Item Off of "{item.text(0)}"', 'Name:')
            if ok and text:
                item.addChild(QTreeWidgetItem([text]))
                category = item.text(0)
                ItemDatabase.createItemsTable(category)
                ItemDatabase.insertItem(category, text)
                self.saveItems()
        return _addSubItem
    
    def saveItems(self):
        try:
            root = self.invisibleRootItem()
            self.recursiveItemSave(root, self.data)
            if not os.path.isdir('db'):
                os.mkdir('db')
            with open(self.JSON_PATH, 'w') as json_file:
                json.dump(self.data, json_file)
            self.data.clear()
        except:
            print(f'ItemTree.saveItems() Error:\n{traceback.format_exc()}\n')

    def recursiveItemSave(self, item, data):
        item_name = item.text(0)
        print(item_name)
        child_count = item.childCount()
        if child_count:
            if item_name and item_name != 'Parts List': 
                data[item_name] = {}
            for i in range(child_count):
                child = item.child(i)
                if item_name and item_name != 'Parts List':
                    self.recursiveItemSave(child, data[item_name])
                else:
                    self.recursiveItemSave(child, data)

    def loadItems(self):
        with open(self.JSON_PATH, 'r') as json_file:
            self.data = json.load(json_file)
            self.recursiveItemLoad(self.root_item, '', self.data)
        return self.root_item

    # Recursive method used to traverse and collect 
    # all of the parent's associated sub directories.
    def recursiveItemLoad(self, last_item:QTreeWidgetItem, key:str, data:dict):
        if data:
            for sub_key, sub_data in data.items():
                item = QTreeWidgetItem([sub_key])
                last_item.addChild(item)
                self.recursiveItemLoad(item, sub_key, sub_data)
        else:
            items = ItemDatabase.items(key)
            for item in items:
                last_item.addChild(QTreeWidgetItem([item]))
        return  
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    tree = ItemTree()
    tree.setColumnCount(1)
    tree.setHeaderLabel('Select a Category to Search From:')
    item = tree.loadItems()
    
    tree.addTopLevelItem(item)
    
    tree.show()
    tree.saveItems()
    print(tree.data)
    sys.exit(app.exec())
    
