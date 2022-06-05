from unicodedata import category
from PySide6 import (QtWidgets)
from PySide6.QtCore import (Signal, Slot, Qt)

from materialize.edit_dialog import (EditDialog)
from materialize.database import ItemDatabase

class TableItem(QtWidgets.QTableWidgetItem):
    def __init__(self, *args):
        super().__init__(*args)
        self._category = ''
    
    def category(self):
        return self._category
    
    Slot(str)
    def setCategory(self, category:str):
        self._category = category

class QuantitySpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._row = 0
    
    def inc(self):
        self.setValue(self.value() + 1)

    @Slot(int)
    def setRow(self, row:int):
        self._row = row 
    
    def row(self):
        return self._row 

class MaterialTable(QtWidgets.QTableWidget):
    QUANTITY_COL = 0
    ITEM_COL = 1
    NOTES_COL = 2 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(self.NoEditTriggers)
        self.setRowCount(0)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Quantity', 'Item', 'Notes'])
        self.horizontalHeaderItem(self.NOTES_COL).setTextAlignment(Qt.AlignLeft)
        self.horizontalHeader().setStretchLastSection(True)
        self.itemDoubleClicked.connect(self.editNotes)
    
    @Slot(TableItem)
    def editNotes(self, item:TableItem):
        if item.column() == self.NOTES_COL:
            descrip_item:TableItem = self.item(item.row(), self.ITEM_COL)
            category_name = descrip_item.category()
            descrip = descrip_item.text()
            edit_dialog = EditDialog(self, item.row(), self.NOTES_COL, 'Edit Notes', 'Notes')
            edit_dialog.exec()
            if edit_dialog.okPressed() and edit_dialog.value:
                ItemDatabase.setNotes(category_name, edit_dialog.value, descrip)
                
    def addItem(self, quantity:int, item_text:str, category:str, notes:str):
        row = self.rowCount()
        self.setRowCount(self.rowCount() + 1)
        quantity_spinbox = QuantitySpinBox(self)
        quantity_spinbox.setValue(quantity)
        quantity_spinbox.setRow(row)
        self.setCellWidget(row, self.QUANTITY_COL, quantity_spinbox)
        item = TableItem(item_text)
        item.setCategory(category)
        self.setItem(row, self.ITEM_COL, item)
        notes_item = TableItem(notes)
        self.setItem(row,self.NOTES_COL, notes_item)
    
    @Slot(int)
    def removeItem(self, item_row:int):
        self.removeRow(item_row)
        for row in range(0,self.rowCount()):
            self.cellWidget(row, self.QUANTITY_COL).setRow(row)
    
    def itemAtRow(self, item:str):
        for row in range(self.rowCount()):
            if item == self.item(row, self.ITEM_COL).text():
                return row  
        return -1
 



        
