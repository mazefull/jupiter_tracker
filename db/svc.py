import psycopg2
import json
import os

class config:
    def __init__(self, data=None):
        self.data = data

    def build_config(self):
        os.system('echo "" >> ./db/postgres.json')

    def get_template(self):
        file = open('./db/postgres_template_config.json', 'w')
        data = json.load(file)
        return data

    def write_config(self):
        self.build_config()
        file = open('./db/postgres.json', 'w')
        file.write(json.dumps(self.get_template()))


    def get_config(self):
        try:
            file = open('./db/postgres.json', 'r')

        except FileNotFoundError:
            self.write_config()

        else:
            data = json.load(file)
            return data["config"]


class postgres:
    def __init__(self, conn=None):
        self.conn = conn

    def connect(self, config):
        conn = psycopg2.connect(
            dbname=config["db_name"],
            user=config["user"],
            password=config["secret"],
            host=config["host"],
            port=config["port"]
        )
        return conn

    def close(self, db):
        cur = db.cursor()
        cur.close()
        db.close()

dbcfg = config().get_config()
db = postgres().connect(dbcfg)
cur = db.cursor()

def dbc(db):
    postgres().close(db)

cur.execute("SELECT version();")
print(cur.fetchone())
cur.close()
db.close()