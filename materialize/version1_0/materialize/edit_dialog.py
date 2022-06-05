from PySide6 import (QtWidgets)

class EditDialog(QtWidgets.QDialog):
    def __init__(self, table: QtWidgets.QTableWidget, row: int, column: int, title='Edit Table Item', tab_text='Edit Item', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self._table = table
        self._row = row 
        self._column = column
        current_value = self._table.item(self._row, self._column).text()
        self.old_value = current_value
        self.value = current_value

        self._ok_pressed = False 

        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        self.edit_tabs = QtWidgets.QTabWidget(self)
        self.edit_tab = QtWidgets.QWidget(self)
        self.edit_layout = QtWidgets.QVBoxLayout(self.edit_tab)

        self.edit_textbox = QtWidgets.QTextEdit(self)
        self.edit_textbox.setPlainText(current_value)

        self.edit_layout.addWidget(self.edit_textbox)

        self.button_row = QtWidgets.QWidget(self)
        self.button_layout = QtWidgets.QHBoxLayout(self.button_row)
        self.button_layout.setContentsMargins(0,0,0,0)

        self.button_filler = QtWidgets.QWidget(self)
        self.button_filler.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.ok_button = QtWidgets.QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.ok)
        self.cancel_button = QtWidgets.QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.close)

        self.button_layout.addWidget(self.button_filler)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.edit_tabs.addTab(self.edit_tab, tab_text)
        self.main_layout.addWidget(self.edit_tabs)
        self.main_layout.addWidget(self.button_row)

    def ok(self):
        self._ok_pressed = True
        text = self.edit_textbox.toPlainText().strip()
        self.value = text 
        self._table.item(self._row, self._column).setText(text)
        self._table.item(self._row, self._column).setToolTip(text)
        self.close()
    
    def okPressed(self):
        return self._ok_pressed 