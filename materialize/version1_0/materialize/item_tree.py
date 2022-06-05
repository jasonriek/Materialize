import os
import sys
import json
import traceback 
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem)

class ItemTree(QTreeWidget):
    JSON_PATH = 'db/categories.json'
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.root_item = QTreeWidgetItem(['Parts List'])
    
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
            self.recursiveItemLoad(self.root_item, self.data)
        return self.root_item

    # Recursive method used to traverse and collect 
    # all of the parent's associated sub directories.
    def recursiveItemLoad(self, last_item:QTreeWidgetItem, data:dict):
        if data:
            for key, sub_data in data.items():
                item = QTreeWidgetItem([key])
                last_item.addChild(item)
                self.recursiveItemLoad(item, sub_data)
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
    
