from pymongo import MongoClient
import pandas as pd
import numpy as np
from sqlalchemy import *
import datetime

db = create_engine('mysql+mysqlconnector://root:123456@localhost/ils')
connection = db.connect()

client = MongoClient('localhost', 27017)

def get_all_id():
	"""Returns a list of book IDs"""
	return [x["_id"] for x in client.Assignment1.Books.find({}, { "_id":1})]

books = pd.DataFrame(np.array(get_all_id()), columns = ["bookID"])
books.to_sql('books', db, if_exists = 'append', index = False)