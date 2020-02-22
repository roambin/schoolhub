import pymongo
from public import config
client = pymongo.MongoClient('mongodb://'+config.MONGO_USER+':'+config.MONGO_PASSWD+'@'+config.MONGO_HOST+'/schoolhub?w=majority')
db = client["schoolhub"]