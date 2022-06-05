import os
import traceback
from materialize.sqlbasics import (SQL, TEXT)


class ItemDatabase:
    PATH = 'db/items.db'
    ITEMS_TABLE_NAME ='ITEMS'
    ITEMS_ID = 'id'
    ITEMS_DESCRIPTION = 'DESCRIPTION'
    ITEMS_NOTES = 'NOTES'

    @staticmethod
    def formatToTableName(table_name:str):
        table_name = table_name.upper().strip()
        table_split = [item.strip() for item in table_name.split() if item.strip()]
        table_name = '_'.join(table_split)
        return table_name

    @staticmethod
    def createItemsTable(category_name:str):
        try:
            table_name = ItemDatabase.formatToTableName(category_name)
            if not os.path.isdir('db'):
                os.mkdir('db')
            SQL.createTable(table_name,
            {ItemDatabase.ITEMS_DESCRIPTION: TEXT,
            ItemDatabase.ITEMS_NOTES: TEXT}, 
            ItemDatabase.PATH)
        except:
            print(f'ItemDatabase.createItemsTable() Error: {traceback.format_exc()}')
    
    @staticmethod
    def insertItem(category_name:str, item:str):
        table_name = ItemDatabase.formatToTableName(category_name)
        if SQL.value(table_name, ItemDatabase.ITEMS_DESCRIPTION, ItemDatabase.ITEMS_DESCRIPTION, item, ItemDatabase.PATH):
            return False 
        SQL.insert(table_name, {
            ItemDatabase.ITEMS_DESCRIPTION: item,
            ItemDatabase.ITEMS_NOTES: '',
        }, ItemDatabase.PATH)
        return True 
    
    @staticmethod
    def items(category_name:str):
        table_name = ItemDatabase.formatToTableName(category_name)
        return SQL.getColumn(table_name, ItemDatabase.ITEMS_DESCRIPTION, ItemDatabase.PATH)
    
    @staticmethod
    def idFromItem(category_name:str, item:str):
        table_name = ItemDatabase.formatToTableName(category_name)
        return SQL.value(table_name, ItemDatabase.ITEMS_ID, ItemDatabase.ITEMS_DESCRIPTION, item, ItemDatabase.PATH)

    @staticmethod
    def categories():
        return SQL.tableNames(ItemDatabase.PATH)
