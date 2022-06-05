import os
import traceback
from sqlbasics import (SQL, TEXT)


class ItemDatabase:
    PATH = 'db/items.db'
    ITEMS_TABLE_NAME ='ITEMS'
    ITEMS_ID = 'id'
    ITEMS_DESCRIPTION = 'DESCRIPTION'
    ITEMS_VENDOR = 'VENDOR'
    ITEMS_NOTES = 'NOTES'
    
    @staticmethod
    def createItemsTable():
        try:
            if not os.path.isdir('db'):
                os.mkdir('db')
            SQL.createTable(ItemDatabase.ITEMS_TABLE_NAME,
            {ItemDatabase.ITEMS_DESCRIPTION: TEXT,
            ItemDatabase.ITEMS_VENDOR: TEXT,
            ItemDatabase.ITEMS_NOTES: TEXT}, 
            ItemDatabase.PATH)
        except:
            print(f'ItemDatabase.createItemsTable() Error: {traceback.format_exc()}')
