import os
import json
import csv 
import traceback
from unicodedata import category

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem)
from PySide6.QtCore import (Qt, QPoint)
from PySide6.QtGui import (QAction)

from materialize.database import ItemDatabase

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
        add_sub_item_action = QAction('Add Sub-Item', self)
        add_sub_item_action.triggered.connect(self.addSubItem(item))
        add_sub_items_action = QAction('Add Sub-Items', self)
        add_sub_items_action.triggered.connect(self.addSubItems(item))
        menu.addAction(show_item_action)
        menu.addSeparator()
        menu.addAction(add_sub_item_action)
        menu.addAction(add_sub_items_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def showItem(self, item:QTreeWidgetItem):
        def _showItem():
            if item.parent():
                category_name = item.parent().text(0)
                item_name = item.text(0)
                print(ItemDatabase.idFromItem(category_name, item_name))
        return _showItem

    def addSubItem(self, item:QTreeWidgetItem):
        def _addSubItem():
            text, ok = QtWidgets.QInputDialog.getText(self, f'Sub-Item Off of "{item.text(0)}"', 'Name:')
            if ok and text:
                item.addChild(QTreeWidgetItem([text]))
                category_text = item.text(0)
                ItemDatabase.createItemsTable(category_text)
                ItemDatabase.insertItem(category_text, text)
                self.saveItems()
        return _addSubItem

    def addSubItems(self, item:QTreeWidgetItem):
        def _addSubItems():
            try:
                category_text = item.text(0)
                path,_ = QtWidgets.QFileDialog.getOpenFileName(self,
                f'Open Items File for "{item.text(0)}"',
                '',
                'CSV (*.csv)')
                if path:
                    with open(path, 'r') as f:
                        reader = csv.reader(f)
                        for line in reader:
                            if line:
                                item_text = line[0].strip()
                                if item_text:
                                    item.addChild(QTreeWidgetItem([item_text]))
                                    ItemDatabase.insertItem(category_text, item_text)

            except Exception as error:
                QtWidgets.QMessageBox.critical(self,
                'Error',
                f'addSubItems() Error: {str(error)}')
        return _addSubItems
    
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

    def recursiveItemLoad(self, last_item:QTreeWidgetItem, key:str, data:dict):
        if data:
            for sub_key, sub_data in data.items():
                item = QTreeWidgetItem([sub_key])
                last_item.addChild(item)
                self.recursiveItemLoad(item, sub_key, sub_data)
            items = ItemDatabase.items(key)
            for item in items:
                if item not in data.keys():
                    last_item.addChild(QTreeWidgetItem([item]))
        else:
            items = ItemDatabase.items(key)
            for item in items:
                last_item.addChild(QTreeWidgetItem([item]))
        return
