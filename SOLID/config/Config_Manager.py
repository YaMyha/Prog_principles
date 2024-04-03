import configparser


class ConfigManager:
    path = "config/config.ini"

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

        with open(self.path, 'w') as config_file:
            self.config.write(config_file)

    def get_config(self):
        self.config.read(self.path)
        config_data = dict(self.config['database'])
        return config_data
