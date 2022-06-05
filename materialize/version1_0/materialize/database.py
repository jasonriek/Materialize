import os
import traceback
from materialize.sqlbasics import (SQL, TEXT)


class ItemDatabase:
    PATH = 'db/items.db'
    ITEMS_TABLE_NAME ='ITEMS'
    ITEMS_ID = 'id'
    ITEMS_DESCRIPTION = 'DESCRIPTION'
    ITEMS_NOTES = 'NOTES'
    CATEGORY_NAMES_TABLE_NAME = 'CATEGORY_NAMES'
    CAT_TABLE_NAME = 'TABLE_NAME'
    CAT_NAME = 'CATEGORY_NAME'

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
    def createCategoryNameTable():
        try:
            if not os.path.isdir('db'):
                os.mkdir('db')
            SQL.createTable(ItemDatabase.CATEGORY_NAMES_TABLE_NAME,
            {ItemDatabase.CAT_TABLE_NAME: TEXT,
            ItemDatabase.CAT_NAME: TEXT}, 
            ItemDatabase.PATH)
        except:
            print(f'ItemDatabase.createCategoryNameTable() Error: {traceback.format_exc()}')    

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
    def insertCategoryName(category_name:str):
        table_name = ItemDatabase.formatToTableName(category_name)
        if SQL.value(ItemDatabase.CATEGORY_NAMES_TABLE_NAME, ItemDatabase.CAT_TABLE_NAME, ItemDatabase.CAT_TABLE_NAME, category_name, ItemDatabase.PATH):
            return False 
        SQL.insert(ItemDatabase.CATEGORY_NAMES_TABLE_NAME, {
            ItemDatabase.CAT_TABLE_NAME: table_name,
            ItemDatabase.CAT_NAME: category_name,
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
    def categoryNames():
        return SQL.getColumn(ItemDatabase.CATEGORY_NAMES_TABLE_NAME,
        ItemDatabase.CAT_NAME,
        ItemDatabase.PATH)
    
    @staticmethod
    def categoryTableNames():
        return SQL.getColumn(ItemDatabase.CATEGORY_NAMES_TABLE_NAME,
        ItemDatabase.CAT_TABLE_NAME,
        ItemDatabase.PATH)

    @staticmethod
    def notes(category_name:str, item:str):
        table_name = ItemDatabase.formatToTableName(category_name)
        return SQL.value(table_name, ItemDatabase.ITEMS_NOTES, ItemDatabase.ITEMS_DESCRIPTION, item, ItemDatabase.PATH)
    
    @staticmethod
    def setNotes(category_name:str, notes:str, item:str):
        table_name = ItemDatabase.formatToTableName(category_name)
        SQL.update(table_name, ItemDatabase.ITEMS_NOTES, notes, ItemDatabase.ITEMS_DESCRIPTION, item, ItemDatabase.PATH)