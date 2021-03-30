import pymongo
import datetime
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sqlalchemy import *

client = pymongo.MongoClient('localhost', 27017)
db = client.Assignment1
books = db.Books


## Index for title search & author, category, year filters.
## Run the following lines once

books.create_index([('title', 'text')], default_language='none')

for x in books.find():
    try:
        yearIndex = x['publishedDate'].year
    except KeyError:
        yearIndex = -1
    books.update_one(x, { "$set": { "yearIndex" : yearIndex } })

books.create_index([ ("authors", 1) ])
books.create_index([ ("categories", 1) ])
books.create_index([ ("yearIndex", 1) ])


engine = create_engine('mysql+mysqlconnector://root:tittimimi(02112002)@localhost/ils')
connection = engine.connect()

def get_all_id():
	"""Returns a list of book IDs"""
	return [x["_id"] for x in books.find({}, { "_id":1})]

sql_books = pd.DataFrame(np.array(get_all_id()), columns = ["bookID"])
sql_books.to_sql('books', engine, if_exists = 'append', index = False)








