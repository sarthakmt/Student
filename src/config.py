''' Connection details for mongodb '''

import pymongo as py

client = py.MongoClient('localhost',27017)
DB = client.studentTracker
DEBUG = True