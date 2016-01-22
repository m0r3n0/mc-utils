from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

# this assumes that you have build the scripts for upgrading on REPO/versions/XXX_whatever
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))

