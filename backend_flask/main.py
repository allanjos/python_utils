import sys
import signal
from log import Log
from config import Config
from web_server import WebServer

Config.load()

class Server:
    def __init__(self):
        Log.info("Server.init()")

        self.webServer = WebServer()

    def start(self):
        Log.info("Server.start()")

        self.webServer.start()

    def stop(self):
        Log.info("Server.stop()")

        self.webServer.stop()

# Main execution

def signalHandler(signr, frame):
    print('Ctrl+C pressed')

    sys.exit(0)

    return

def main():
    signal.signal(signal.SIGINT, signalHandler)

    server = Server()

    server.start()

if __name__ == "__main__":
    main()