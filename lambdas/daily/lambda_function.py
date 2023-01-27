import json
import sqlalchemy as db

from  data.credentials import DBCredentials

def lambda_handler(event, context):
    method = event["httpMethod"]
    if(method == "GET"):
        awsdb = AWSDatabase()
        print(awsdb.queryAllData())
    elif(method == "POST"):
        pass
        
    
class AWSDatabase:
    
    def __init__(self) -> None:
        self.cred = DBCredentials()
        self.engine = db.create_engine(f'mysql+pymysql://{self.cred.USER}:{self.cred.PASS}@{self.cred.URL}:{self.cred.PORT}/{self.cred.DB_NAME}')
        self.conn = self.engine.connect()
        self.metadata = db.MetaData()
        self.division= db.Table("Daily", self.metadata, autoload=True, autoload_with=self.engine)
    
    def queryAllData(self):
        """ returns all data in database

        Returns:
            list: contains a list with every item in database
        """        
        query =  self.division.select()
        exe = self.conn.execute(query)
        return exe.fetchall()

