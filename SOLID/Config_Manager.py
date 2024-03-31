import configparser


class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.create_config()

    def create_config(self):
        self.config['database'] = {
            "drivername": "postgresql+psycopg2",
            "host": "localhost",
            "port": 5432,
            "username": "postgres",
            "password": "YuWlNvrGs",
            "database": "dubadidib"
        }

        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)

    def get_config(self):
        self.config.read('config.ini')
        config_data = dict(self.config['database'])
        return config_data
