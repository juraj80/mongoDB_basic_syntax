**Installing MongoDB on macOS**

1. install homebrew at brew.sh
2. `brew install mongodb`
3. Start MongoDB
    - `brew services start mongodb`                                                                         
             OR               
    - `mongod --config /usr/local/etc/mongo.conf`
4. Config is at /usr/local/etc/mongod.conf

**Installing MongoDB on Linux**

1. Visit Ubuntu setup page at mongodb.com
2. Add key: 
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```
3. Add list file, careful on version: 
```
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```
4. Update: `sudo apt-get update`
5. Install: `sudo apt install mongodb-org`
6. Start service: `sudo service mongod start`
7. Review config: `/etc/mongod.conf`

**Directions to restore DB into MongoDB**

To restore any of these databases to MongoDB, you'll need to uncompress them and then run this command:

```
mongorestore --drop --db DATABASE /path/to/unziped/dir
```


**Connecting**

````
$ mongo
> show dbs
> use DATABASE
> show collections
````

**Basic querying**
````
db.Test.drop()
db.Book.find().limit(1).pretty()
db.Book.find({"Title":'From the Corner of His Eye'}).count()
db.Book.find({"Title":'From the Corner of His Eye'},{Title:1, ISBN:1}).pretty()
db.Book.find({"Title":'From the Corner of His Eye'},{Title:1, ISBN:1, _id:0}).pretty()
db.Book.find({"Title":'From the Corner of His Eye', ISBN: '0553801341'},{Title:1, ISBN:1, _id:0}).pretty()
db.Book.find({"Ratings.UserId":ObjectId("525867753a93bb2198148dc0")},{Title:1,_id:0})`
````

Queries are done via find. Pass prototypical JSON documents

```
> db.Book.find({Title: 'From the Corner of His Eye'})
{
	"_id" : ObjectId("525867313a93bb2198103c40"),
	"ISBN" : "0553582747",
	"Title" : "From the Corner of His Eye",
	"Author" : "Dean Koontz",
	...
},
{
	"_id" : ObjectId("525867343a93bb21981066e7"),
	"ISBN" : "0553801341",
	"Title" : "From the Corner of His Eye",
	"Author" : "Dean R. Koontz",
	...
},
...
```

**Querying (AND)**

```
> db.Book.find({Title: 'From the Corner of His Eye', ISBN: '0553582747'})
{
	"_id" : ObjectId("525867313a93bb2198103c40"),
	"ISBN" : "0553582747",
	"Title" : "From the Corner of His Eye",
	"Author" : "Dean Koontz",
```

**Querying (sub-documents)**
```
> db.Book.find({"Ratings.UserId":ObjectId("525867733a93bb219814604e")})
{
    "_id" : ObjectId("525867313a93bb2198103c40"),
    "ISBN" : "0553582747",
    "Title" : "From the Corner of His Eye",
    "Author" : "Dean Koontz",
    "Published" : ISODate("2001-01-01T08:00:00.000Z"),
    "Publisher" : ObjectId("5258672d3a93bb21980ffff5"),
    "Ratings" : [ 
        {
            "UserId" : ObjectId("525867733a93bb219814604e"),
            "Value" : 7
        }, 
        {
            "UserId" : ObjectId("525867733a93bb21981466a0"),
            "Value" : 5
        }, 
        {
            "UserId" : ObjectId("525867733a93bb2198146914"),
            "Value" : 0
        }, 
        ...
```
**Advanced queries**

Q: How many books have been rated with 9?

`> db.Book.find({"Ratings.Value": 9}).count()
`

Q: How many books have been rated with 8 or above?

`> db.Book.find({"Ratings.Value": {$gte: 8}}).count()
`

Q: How many books have been rated above 8?

`> db.Book.find({"Ratings.Value": {$gt: 8}}).count()
`

Q: How many books have primes ratings ?

`> db.Book.find({"Ratings.Value": {$in: [1,2,3,5,7] }  }).count()
`

**Query Selectors**

Comparison
```
Name	Description
$eq     Matches values that are equal to a specified value.
$gt     Matches values that are greater than a specified value.
$gte	Matches values that are greater than or equal to a specified value.
$in     Matches any of the values specified in an array.
$lt	Matches values that are less than a specified value.
$lte	Matches values that are less than or equal to a specified value.
$ne	Matches all values that are not equal to a specified value.
$nin	Matches none of the values specified in an array.
```
Logical
```
Name	Description
$and	Joins query clauses with a logical AND returns all documents that match the conditions of both clauses.
$not	Inverts the effect of a query expression and returns documents that do not match the query expression.
$nor	Joins query clauses with a logical NOR returns all documents that fail to match both clauses.
$or	Joins query clauses with a logical OR returns all documents that match the conditions of either clause.
```
https://docs.mongodb.com/manual/reference/operator/query/


**Projections**

```
> db.Book.find({...},{ISBN:1,Title:1})

{
    "_id" : ObjectId("525867313a93bb2198103c40"),
    "ISBN" : "0553582747",
    "Title" : "From the Corner of His Eye"
}

{
    "_id" : ObjectId("525867323a93bb2198104f24"),
    "ISBN" : "3404136012",
    "Title" : "Wintermond. Unheimlicher Roman."
}

{
    "_id" : ObjectId("525867323a93bb2198104f25"),
    "ISBN" : "3453131169",
    "Title" : "Fl�?¼stern in der Nacht."
}
```

**Exact subdocument matches**

That's not the AND we wanted

```
> db.Book.find({"Ratings.Value":9,"Ratings.UserId":600)})

{...
    "Ratings" : [ 
        {
            "UserId" : 700,
            "Value" : 5
        }, 
        {
            "UserId" : 200,
            "Value" : 9
        }, 
        {
            "UserId" : 600,
            "Value" : 0
        }, ...
},
{...
    "Ratings" : [ 
        {
            "UserId" : 600,
            "Value" : 9
        }, ... 
},

//more results
```

We want $elemMatch

```
> db.Book.find({Ratings: {$elemMatch: {UserId:600), Value: 9} }})

{...
    "Ratings" : [ 
        {
            "UserId" : 600,
            "Value" : 9
        }, ... 
},

//more results
```

**Sorting**


`> db.Book.find().sort( { Published: -1} )
`
```
> db.Book.find().sort( {Title:1, Published: -1} )

{
    "_id" : ObjectId("525867433a93bb219811638a"),
    "Title" : "!%@ (A Nutshell handbook)",
    "Published" : ISODate("1994-01-01T08:00:00.000Z")
}

/* 2 */
{
    "_id" : ObjectId("525867563a93bb2198129ecf"),
    "Title" : "!%@ (A Nutshell handbook)",
    "Published" : ISODate("1993-01-01T08:00:00.000Z")
}

/* 3 */
{
    "_id" : ObjectId("5258674c3a93bb219811f52c"),
    "Title" : "!Arriba! Comunicacion y cultura",
    "Published" : ISODate("1996-01-01T08:00:00.000Z")
}
```

**Inserts**

If we don't specify key: _id, MongoDB will generate it.
```
> db.Book.insert({Title: 'From the Corner of My Eye', ...'})

> db.Book.find()...

{
    "_id" : ObjectId("5c0437172d5576eb08ded262"),
    "Title" : "From the Corner of My Eye",
    "ISBN" : "0440234743",
    "Author" : "Steve Jobs"
    //...
}
```

**Whole document Update**

```
> db.Book.update(
        {_id : ObjectId("5c0437172d5576eb08ded262") },                                            # First argument (required) is the WHERE clause
        {Title: 'From the Corner of My Eye 2nd Edition', ISBN: '0000000000',Author: 'Mr.NoName'}, # Next argument (required) is the new document
        {upsert: true, multi: true} )                                                             # Additional options may not be specified

> db.Book.find()...

{
    "_id" : ObjectId("5c0437172d5576eb08ded262"),
    "Title" : "From the Corner of My Eye 2nd Edition",
    "ISBN" : "0000000000",
    "Author" : "Mr.NoName"
}

```

**Deleting documents**

```
> db.Book.deleteOne( {"_id" : ObjectId("5c0437172d5576eb08ded262")} )

> db.Book.deleteMany( {"Title" : "Some title"} )
```

**Atomic updates**



```
> var book = db.getCollection('BookReads').findOne({'ISBN':'94724773501'})
> book.ReadCount += 1
> db.getCollection('BookReads').update({'_id':book._id},book)
> db.getCollection('BookReads').find({'ISBN':'94724773501'})


{
    "_id" : ObjectId("5c0506042d5576eb08ded263"),
    "ISBN" : "94724773501",
    "ReadCount" : 1.0
}
```

Better way for update is to use operators.

```
> db.getCollection('BookReads').find({'ISBN':'94724773501'})
> db.getCollection('BookReads').update({'_id':book._id},{$inc: {ReadCount: 1}})
> db.getCollection('BookReads').find({'ISBN':'94724773501'})


{
    "_id" : ObjectId("5c0506042d5576eb08ded263"),
    "ISBN" : "94724773501",
    "ReadCount" : 2.0
}

```


Field
```
Name	        Description
$currentDate	Sets the value of a field to current date, either as a Date or a Timestamp.
$inc	        Increments the value of the field by the specified amount.
$min	        Only updates the field if the specified value is less than the existing field value.
$max	        Only updates the field if the specified value is greater than the existing field value.
$mul	        Multiplies the value of the field by the specified amount.
$rename	        Renames a field.
$set	        Sets the value of a field in a document.
$setOnInsert	Sets the value of a field if an update results in an insert of a document. Has no effect on update operations that modify existing documents.
$unset	        Removes the specified field from a document.
```


Array

```
Operators

Name	        Description
$	        Acts as a placeholder to update the first element that matches the query condition.
$[]	        Acts as a placeholder to update all elements in an array for the documents that match the query condition.
$[<identifier>]	Acts as a placeholder to update all elements that match the arrayFilters condition for the documents that match the query condition.
$addToSet	Adds elements to an array only if they do not already exist in the set.
$pop	        Removes the first or last item of an array.
$pull	        Removes all array elements that match a specified query.
$push	        Adds an item to an array.
$pullAll        Removes all matching values from an array.
```

https://docs.mongodb.com/manual/reference/operator/update/
```
> db.Test.insert( { Title: 'A popular book', ViewCount: 0} )
> db.Test.find()

{
    "_id" : ObjectId("5c050ca62d5576eb08ded264"),
    "Title" : "A popular book",
    "ViewCount" : 0.0
}

> db.Test.update( {_id:ObjectId("5c050ca62d5576eb08ded264")}, {$inc: {ViewCount: 1}})
> db.Test.update( {_id:ObjectId("5c050ca62d5576eb08ded264")}, {$inc: {ViewCount: 1}})
> db.Test.update( {_id:ObjectId("5c050ca62d5576eb08ded264")}, {$inc: {ViewCount: 1}})

{
    "_id" : ObjectId("5c050ca62d5576eb08ded264"),
    "Title" : "A popular book",
    "ViewCount" : 3.0
}

```

#Introduction to PyMongo

_pymongo_ is the core package to access MongoDB

Features include
- Connect to database, replicate set, or shard
- Query and generally perform CRUD
- Other admin operations
- Connection pooling

https://github.com/mongodb/mongo-python-driver

Some CRUD operations

```
import pymongo

conn_str = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn_str)

db = client.the_small_bookstore

# now we can operate on the db via collections
print('There are {} books'.format(db.books.count() ))
print('First book: {}'.format(db.books.find_one() ))
print('Book by ISBN: {}'.format(db.books.find_one({'ISBN': '0399135782'}) ))

res = db.books.insert_one({'title': 'New book','ISBN': '1234567890'})

{
    "_id" : ObjectId("5c0518e2bd09bd34373e8528"),
    "title" : "New book",
    "ISBN" : "1234567890"
}
 
```

**Connection string examples**

Connect to the server mongo_server on default port within a virtual private network or in the same data center zone or cloud hosting like a Digital Ocean

`conn_str = 'mongodb://mongo_server'
`

Connect to mongo_server on an alternate port

`conn_str = 'mongodb://mongo_server:2000' 
`

Use authentication when connecting

`conn_str = 'mongodb://jeff:supersecure@mongo_server:2000' 
`

Connect to a replicate set

`conn_str = 'mongodb://mongo_server:2000, mongo_server:2001, mongo_server2:2002/?replicaSet=prod' 
`

**Atomic updates from Python (using the in_place operators)**
```
import pymongo
conn_str = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn_str)
db = client.the_small_bookstore

res = db.books.insert_one({'title': "New Book", 'isbn': "1234567890"})
db.books.update({'isbn': "1234567890"}, {'$addToSet': {'favorited_by': 1001}})
db.books.update({'isbn': "1234567890"}, {'$addToSet': {'favorited_by': 1002}})
db.books.update({'isbn': "1234567890"}, {'$addToSet': {'favorited_by': 1002}})

{'_id': ObjectId('5c0646b4bd09bd3d6f1a371b'), 'title': 'New Book', 'isbn': '1234567890', 'favorited_by': [1001, 1002]}

```

**EXAMPLE: Atomic vs Whole document update from Python**

```
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

'''An atomic, in place update'''

db.books.update({'isbn': '73738947385'}, {'$addToSet': {'favorited_by': 101} } ) # addToSet Mongo operator in Python with quotes
book = db.books.find_one({'isbn': '73738947385'})
print(book)


{'_id': ObjectId('5c0518e3bd09bd34373e8529'), 'title': 'The second book', 'isbn': '73738947385', 'favorited_by': [101]}
```

Mapping from MongoDB api to PyMongo documentation

http://api.mongodb.com/python/current/api/pymongo/collection.html

_Note: If we want to write an app, PyMongo could be our data access layer, the low level way to talk to MongoDB._

# Modeling and document design
![alt text](pic28.png)


![alt text](/Users/jurajklucka/PycharmProjects/mongoDB_basic_syntax/pic29.png)

https://github.com/juraj80/mongoDB_basic_syntax/raw/master/pic28.png
