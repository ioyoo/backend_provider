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
        """ returns all data in database

        Returns:
            list: contains a list with every item in database
        """        
        query =  self.division.select()
        exe = self.conn.execute(query)
        return exe.fetchall()
    
    def head(self, number=5):
        """ returns {number} data in database

        Args:
            number (int, optional): Number of items to return. Defaults to 5.

        Returns:
            list: contains a list with the {number} of item in database
        """        
        query =  self.division.select()
        exe = self.conn.execute(query)
        return exe.fetchmany(number)
    
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