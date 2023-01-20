import json
from data.databases import HourlyDB

def lambda_handler(event, context):
    db = HourlyDB()
    print(str(db.getColumnNames()))

lambda_handler(1,1)