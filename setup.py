# This class is set-up your database configuration.
import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cogs.utils import models


def loadDbConfig():
    with open('postgresql.json') as f:
        return json.load(f)

def main():
    db = loadDbConfig()

    Base = declarative_base()

    print ('Connecting to DB')
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(db['user'], db['password'], db['hostname'], db['database']), echo=True)

    models.Tag.__table__.create(engine, checkfirst=True)
    models.User.__table__.create(engine, checkfirst=True)
    models.Rank.__table__.create(engine, checkfirst=True)
    models.Role.__table__.create(engine, checkfirst=True)
    models.Level.__table__.create(engine, checkfirst=True)
    models.Topic.__table__.create(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)

    # Try doing an initial insert for levels (up to 50)
    ranks = []
    for i in range(50):
        xp = 100 * int(round(pow(i, 1.2)))
        rank = models.Rank(xp=xp)
        ranks.append(rank)

    # Try addding the ranks
    db = Session()
    if db.query(models.Rank).count() == 0:
        try:
            db.add_all(ranks)
            db.commit()
        except Exception as e:
            print (e)


if __name__ == '__main__':
    main()