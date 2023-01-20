import json
from data.databases import HourlyDB

def lambda_handler(event, context):
    db = HourlyDB()
    print(str(db.queryAllData()))

lambda_handler(1,1)