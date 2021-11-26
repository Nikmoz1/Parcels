import configparser


class Config:
    @staticmethod
    def auth_conf():
        config = configparser.ConfigParser()
        config.read("settings.ini")
        return config["Authorization"]
