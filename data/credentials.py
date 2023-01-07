import yaml
import os


class DBCredentials:
    USER = ""
    PASS = ""
    URL = ""
    PORT = ""
    DB_NAME = ""
    CRED_PATH = 'backend_provider\private\credentials.yaml'

    def __init__(self, cred_path=CRED_PATH) -> None:
        self.CRED_PATH = cred_path
        cred_full_path = os.path.join(os.getcwd(), cred_path)
        with open(cred_full_path) as credentials_raw:
            try:
                credentials = yaml.safe_load(credentials_raw)
                self.USER = credentials['username']
                self.PASS = credentials['password']
                self.URL = credentials['access_url']
                self.PORT = credentials['port']
                self.DB_NAME = credentials['db_name']
            except yaml.YAMLError as exc:
                print(exc)

    def __repr__(self) -> str:
        return f' User: {self.USER}, Pass: {self.PASS[0:-4]}*****, URL: {self.URL}, Port: {self.PORT}, Database Name: {self.DB_NAME}'
