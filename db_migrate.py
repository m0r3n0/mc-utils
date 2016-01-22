import imp
import os
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URI

# get current db version
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# set new name of the migration script according to version
migration = os.path.join(os.path.join(SQLALCHEMY_MIGRATE_REPO, 'versions'), '%03d_migration.py' % (v+1))
# track differences between old and existing model: do not rename fields, just add or remove models or fields
tmp_module = imp.new_module('old_model')
old_module = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_module, tmp_module.__dict__)
# build the migration script and write it
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
# upgrade the database to the existing model using the scripts created in the migration
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))


