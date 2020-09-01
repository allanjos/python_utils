import threading
from flask import Flask
from flask import json
from flask import request
from database import ItemsDatabase
from log import Log
from config import Config

Config.load()

class WebServer:
    def __init__(self):
        Log.info("WebServer.init()")

        self.itemsDb = ItemsDatabase()

        self.app = Flask(__name__)

    def start(self):
        Log.info("WebServer.start()")

        self.itemsDb.start()

        self.app.add_url_rule('/', methods=['GET'], view_func=self.getDocumentRoot)
        self.app.add_url_rule('/api', methods=['GET'], view_func=self.getDocumentRoot)
        self.app.add_url_rule('/api/item', methods=['GET'], view_func=self.getItemsList)
        self.app.add_url_rule('/api/item/<_id>', methods=['GET'], view_func=self.getItemInfo)
        self.app.add_url_rule('/api/item', methods=['POST'], view_func=self.postItem)
        self.app.add_url_rule('/api/item/delete', methods=['POST'], view_func=self.deleteItem)

        self.serverThread = threading.Thread(target=self.serverThreadCallback, args=(1,))

        self.serverThread.start()

    def serverThreadCallback(self, name):
        Log.info("WebServer.serverThreadCallback() name=" + str(name))

        self.app.run(host=Config.data()['webserver']['host'], port=Config.data()['webserver']['port'], debug=False, use_reloader=False)

    def stop(self):
        Log.info("WebServer.stop()")

        self.itemsDb.stop()

        func = request.environ.get('werkzeug.server.shutdown')

        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        func()

        self.serverThread.join()

    def getDocumentRoot(self):
        Log.info("WebServer.getDocumentRoot()")

        return {
            "application": Config.data()['app']['name'],
            "version": Config.data()['app']['version']
        }

    def getItemsList(self):
        Log.info("WebServer.getItemsList()")

        items = self.itemsDb.getItems()

        return {
            "result": "0",
            "message": "get-items",
            "data": items
        }

    def getItemInfo(self, _id):
        Log.info("WebServer.getItemInfo()")

        item = self.itemsDb.getItem(_id)

        return {
            "result": "0",
            "message": "get-item",
            "data": item
        }

    def postItem(self):
        Log.info("WebServer.postItem()")

        data = request.json

        dbResult = self.itemsDb.saveItem(data)

        return {
            "result": "0",
            "message": "post-item",
            "data": dbResult
        }

    def deleteItem(self):
        Log.info("WebServer.deleteItem()")

        data = request.json

        Log.info("data:")
        Log.info(data)

        dbResult = self.itemsDb.deleteItem(data)

        return {
            "result": dbResult['result'],
            "message": "delete-item",
            "data": dbResult['deleted']
        }