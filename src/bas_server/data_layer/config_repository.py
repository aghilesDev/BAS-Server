import json
class FileRepository:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def load_data(self):
        with open(self.file_path, "r+") as file:
            # Reading from a file
            self.data = json.loads(file.read())

    def save_data(self):
        with open(self.file_path, "w") as file:
            data_string = json.dumps(self.data)
            file.write(data_string)
            file.close()

    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value


class ConfigurationFactory:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            file_path = "src/data/config.json"
            cls._instance = FileRepository(file_path)
            cls._instance.load_data()
        return cls._instance
