#import Exception
class CredentialStore:
    def __init__(self, clickup_api_key, google_credentials):
        self.clickup_api_key = clickup_api_key
        self.google_credentials = google_credentials


class CredentialStoreFactory:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            Exception("The factory has not been intialized. Before calling this method, intialize the Factory with intitialtize(...) method")
        return cls._instance

    @classmethod
    def initialize(cls,clickup_api_key, google_credentials):
        cls._instance = CredentialStore(clickup_api_key, google_credentials)

