from PySide6 import (QtWidgets)
from PySide6.QtCore import (Signal, Slot, Qt)

class QuantitySpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._row = 0

    @Slot(int)
    def setRow(self, row:int):
        self._row = row 
    
    def row(self):
        return self._row 

class MaterialTable(QtWidgets.QTableWidget):
    QUANTITY_COL = 0
    ITEM_COL = 1
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRowCount(0)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Quantity', 'Item'])
        self.horizontalHeaderItem(self.ITEM_COL).setTextAlignment(Qt.AlignLeft)
        self.horizontalHeader().setStretchLastSection(True)
    


    def addItem(self, quantity:int, item:str):
        row = self.rowCount()
        self.setRowCount(self.rowCount() + 1)
        quantity_spinbox = QuantitySpinBox(self)
        quantity_spinbox.setValue(quantity)
        quantity_spinbox.setRow(row)
        self.setCellWidget(row, self.QUANTITY_COL, quantity_spinbox)
        self.setItem(row, self.ITEM_COL, QtWidgets.QTableWidgetItem(item))
    
    @Slot(int)
    def removeItem(self, item_row:int):
        self.removeRow(item_row)
        for row in range(0,self.rowCount()):
            self.cellWidget(row, self.QUANTITY_COL).setRow(row)
 



        
