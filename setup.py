# This class is set-up your database configuration.
import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from cogs.utils import models


def loadDbConfig():
    with open('postgresql.json') as f:
        return json.load(f)

def main():
    db = loadDbConfig()

    Base = declarative_base()

    print ('Connecting to DB')
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(db['user'], db['password'], db['hostname'], db['database']), echo=True)

    models.Tag.__table__.create(engine)

if __name__ == '__main__':
    main()