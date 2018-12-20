import pymongo
conn_str = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn_str)
db = client.the_small_bookstore


if db.books.count() == 0:
    print("Inserting data")
    # insert some data...
    r = db.books.insert_one({'title': 'The first book', 'isbn': '73738947384'})
    print(r, type(r))
    r = db.books.insert_one({'title': 'The second book', 'isbn': '73738947385'})
    print(r.inserted_id)
else:
    print("Books already inserted, skipping")


''' To pull whole document back and update'''

# book = db.books.find_one({'isbn': '73738947384'})
# # print(type(book),book)
# # book['favorited_by'] = []
# book['favorited_by'].append(42)
# db.books.update({'_id':book.get('_id')},book)
# book = db.books.find_one({'isbn': '73738947384'})
# print(book)

''' An atomic, in place update '''

db.books.update({'isbn': '73738947385'}, {'$addToSet': {'favorited_by': 101} } ) # addToSet Mongo operator in Python with quotes
book = db.books.find_one({'isbn': '73738947385'})
print(book)
