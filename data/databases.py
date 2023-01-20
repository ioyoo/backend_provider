from .credentials import DBCredentials
import sqlalchemy as db

class AWSDatabase:
    
    def __init__(self, table) -> None:
        self.cred = DBCredentials()
        self.engine = db.create_engine(f'mysql+pymysql://{self.cred.USER}:{self.cred.PASS}@{self.cred.URL}:{self.cred.PORT}/{self.cred.DB_NAME}')
        self.conn = self.engine.connect()
        self.metadata = db.MetaData()
        self.division= db.Table(table, self.metadata, autoload=True, autoload_with=self.engine)
    
    def queryAllData(self):
        pass
    
    def getColumnNames(self):
        return self.division.columns.keys()

class HourlyDB(AWSDatabase):
    def __init__(self) -> None:
        super().__init__('Hour')
    
    def queryAllData(self):
        return super().queryAllData()
        
class WeeklyDB(AWSDatabase):
    def __init__(self) -> None:
        super().__init__()
        
class MonthlyDB(AWSDatabase):
    def __init__(self) -> None:
        super().__init__()
        
class YearlyDB(AWSDatabase):
    def __init__(self) -> None:
        super().__init__()