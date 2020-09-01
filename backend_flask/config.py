import json

class Config:
    ''' Configuration class '''

    configFilePath = 'config/config.json'
    configData = None
    loaded = False

    @staticmethod
    def load():
        print('Config.load()')

        if (Config.loaded):
            print('Configuration is already loaded.')
            return
        else:
            print('Trying to load configuration...')

        with open(Config.configFilePath) as configFile:
            Config.configData = json.load(configFile)

        Config.loaded = True

    @staticmethod
    def data():
        return Config.configData