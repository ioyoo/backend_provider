import json
import sqlalchemy as db
import requests
from datetime import datetime
from data.credentials import DBCredentials

# TODO refactor class to create standard for all lambdas


def get_top100():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(
        "https://api.nasdaq.com/api/quote/list-type/nasdaq100", headers=headers)
    return [stock["symbol"] for stock in res.json()['data']['data']['rows']]


def rawToJson(raw_data):
    """ transforms database data into a readable json

    Args:
        raw_data (Legacy_row): db format

    Returns:
        dict: json format for data obtained
    """
    tuple_data = [tuple(elem for elem in item) for item in raw_data]
    row_data = {}
    data = {}
    for id, row in enumerate(tuple_data):
        row_data = {"hour": row[0].hour,
                    "minute": row[0].minute,
                    "second": row[0].second}
        for i in range(1, len(row)):
            row_data[i] = row[i]
        data[id] = row_data
    return data


def jsonToDB(data: dict):
    """ Adds remaining data to data received ( time, stocks with no values )

    Args:
        data (dict): data send from data gatherer

    Returns:
        data: full data
    """
    names = get_top100()
    for name in names:
        if name not in data.keys():
            data[name] = 0
    data["DATE"] = datetime.now().strftime("%H:%M:%S")
    return data


class AWSDatabase:

    def __init__(self) -> None:
        self.cred = DBCredentials()
        self.engine = db.create_engine(
            f'mysql+pymysql://{self.cred.USER}:{self.cred.PASS}@{self.cred.URL}:{self.cred.PORT}/{self.cred.DB_NAME}')
        try:
            self.metadata = db.MetaData()
            self.division = db.Table(
                "Daily", self.metadata, autoload=True, autoload_with=self.engine)
        except Exception:
            print("Table doesn't exist: Daily")

    def queryAllData(self):
        """ returns all data in database

        Returns:
            list: contains a list with every item in database
        """
        query = self.division.select()
        with self.engine.connect() as conn:
            exe = conn.execute(query)
            raw_data = exe.fetchall()
        return rawToJson(raw_data)

    def postData(self, data):
        with self.engine.connect() as conn:
            result = conn.execute(
                db.insert(self.division),
                [
                    jsonToDB(data)
                ]
            )
        print("RESULT: " + result)
        # print(jsonToDB(data))

    def _createTable(self):
        # only to create table
        names = get_top100()
        names.sort()
        metadata = db.MetaData()
        columns = [db.Column(name, db.SMALLINT) for name in names]
        columns.insert(0, db.Column("DATE", db.TIME, primary_key=True))
        daily_table = db.Table(
            "Daily",
            metadata,
            *columns
        )
        metadata.create_all(self.engine)


def create_response(code, data="{}", header="we are"):
    return {
        "statusCode": code,
        "headers": {
            "well": header
        },
        "body": json.dumps(data)
    }


def lambda_handler(event, context):
    try:
        method = event["httpMethod"]
        awsdb = AWSDatabase()
        if (method == "GET"):
            return create_response("200", awsdb.queryAllData())
        elif (method == "POST"):
            awsdb.postData(event["body"])
            # awsdb._createTable()
            return create_response("200")
    except TypeError:
        return create_response(404)


print(lambda_handler({"httpMethod": "POST",
                      "body": {"ABNB": 22}
                      }, 2))
