import pymongo

conn_str = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn_str)

db = client.the_small_bookstore

if db.books.count() == 0:
    print("Inserting data")
    # insert some data...
    r = db.books.insert_one({'title': 'The first book','isbn': '73738947384'})
    print(r, type(r))
    r = db.books.insert_one({'title': 'The second book','isbn': '73738947385'})
    print(r.inserted_id)
else:
    print("Books already inserted, skipping")