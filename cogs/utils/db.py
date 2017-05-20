from sqlalchemy import create_engine
import json

# TODO: Fix usage of global
engine = None

def loadDB(user, password, hostname, dbname):
    global engine
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, hostname, dbname))
