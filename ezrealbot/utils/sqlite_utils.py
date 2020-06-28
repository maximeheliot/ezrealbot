import warnings
import os
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from ezrealbot.utils import base_folder

Base = declarative.declarative_base()

# Opening the database
if 'PYTEST_CURRENT_TEST' in os.environ:
    database_location = os.path.join(base_folder, 'ezreal_schema_test.db')
    try:
        os.remove(database_location)
    except PermissionError:
        warnings.warn('Test database open in another program, using it as-is')
    except FileNotFoundError:
        pass
else:
    database_location = os.path.join(base_folder, 'ezreal_schema.db')

engine = sqlalchemy.create_engine('sqlite:///{}'.format(database_location))

# Creating an easy access function
get_session = orm.sessionmaker(bind=engine)


# Defining the function to call at the end of the sqlite initialization
def initialize_sql():
    Base.metadata.create_all(engine)