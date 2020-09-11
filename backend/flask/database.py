import sys
import pymongo
from log import Log
from config import Config
import bson
from bson import json_util
from bson import objectid

Config.load()

class ItemsDatabase:
    ''' Items database class '''

    collectionName = ''

    def __init__(self):
        Log.dbg("ItemsDatabase.__init__()")

        self.client = None

        self.db = None

        self.started = False

    def __del__(self):
        Log.dbg("ItemsDatabase.__del__()")

        self.stop()

    def start(self):
        Log.info("ItemsDatabase.start()")

        if (self.started):
            return

        try:
            Log.info("Configuration data:")
            Log.info(Config.data())

            self.client = pymongo.MongoClient(Config.data()['db']['host'], Config.data()['db']['port'])

            self.db = self.client[Config.data()['db']['dbname']]

            self.started = True

        except Exception as e:
            Log.exception('Exception ocurred in database connection.')
            Log.exception('Exception: ' + e)
            Log.exception('Traceback: ' + e.with_traceback)

            sys.exit(1)

    def getItems(self):
        Log.info("ItemsDatabase.getItems()")

        try:
            items = self.db['items'].find()

            result = []

            for item in items:
                result.append({
                    '_id': str(item['_id']),
                    'name': item['name'],
                    'price': item['price']
                })

            return result

        except Exception as e:
            Log.error(e)

            return []

    def getItem(self, _id):
        Log.info("ItemsDatabase.getItem()")
        Log.info("Item ID: " + _id)

        try:
            items = self.db['items'].find({'_id': objectid.ObjectId(_id)})

            if (items is None or items.count() < 1):
                return json_util.dumps({})

            item = items[0]

            result = {
                'name': item['name'],
                'price': item['price']
            }

            Log.info("y")

            Log.info("result:")
            Log.info(result)

            return result

        except bson.errors.InvalidId as e:
            Log.error(e)

            return {}

        except Exception as e:
            Log.error(e)

            return {}

    def saveItem(self, item):
        Log.info("ItemsDatabase.saveItem()")
        Log.info("item:")
        Log.info(item)

        if 'name' not in item:
            Log.info("Invalid item name")
            return

        if 'price' not in item:
            Log.info("Invalid item price")
            return

        itemId = objectid.ObjectId()

        dbResult = self.db['items'].insert({'_id': itemId, 'name': item['name'], 'price': item['price']})

        return str(itemId)

    def deleteItem(self, data):
        Log.info("ItemsDatabase.deleteItem()")
        Log.info("item id:" + data['_id'])

        dbResult = self.db['items'].delete_one({'_id': objectid.ObjectId(data['_id'])})

        if dbResult is None:
            return {
                "result": -1,
                "deleted": 0
            }

        return {
            "result": 0,
            "deleted": dbResult.deleted_count
        }

    def stop(self):
        Log.info("ItemsDatabase.stop()")

        if self.client is not None:
            self.client.close()

            self.started = False