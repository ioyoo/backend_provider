import json
import sqlalchemy as db
from  data.credentials import DBCredentials

def rawToJson(raw_data):
    tuple_data = [tuple(elem for elem in item) for item in raw_data]
    row_data = {}
    data = {}
    for id, row in enumerate(tuple_data):
        row_data = {"hour" : row[0].hour,
                "minute": row[0].minute,
                "second" : row[0].second}
        for i in range (0, len(row)):
            row_data[i] = row[i]
        data[id] = row_data
    return data
    
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
        raw_data = exe.fetchall()
        self.conn.close()
        return rawToJson(raw_data)

    def postData(self, data):
        pass

def create_response(code, data = "{}", header="we are"):
    return {
        "statusCode": code,
        "headers": {
            "well" : header
        },
        "body": json.dumps(data)
    }
    
def lambda_handler(event, context):
    try:
        method = event["httpMethod"]
        awsdb = AWSDatabase()
        if(method == "GET"):
            return create_response("200", awsdb.queryAllData())
        elif(method == "POST"):
            awsdb.postData
    except TypeError:
        return create_response(404)