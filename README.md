#MongoDB with Python


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
![alt text](src/pic28.png)


![alt text](src/pic29.png)

**To embed or not to embed (normalized) data?**

1. is the embedded data wanted **80% of the time**?
2. How often do you want the embedded
   data **without the containing document**? (if often -> normalize)
3. Is the embedded data **a bounded set**? 
4. Is that bound **small**?
5. **How varied** are your queries? (if much -> normalize)
6. Is this an **integration DB** or an **application DB**? 


Do we have an integration database?
![alt text](src/pic30.png)
Especially in large enterprises, we'll see that they use databases almost as a means of inter-application communication,
so maybe we have this huge relational database that lives in the center with many, many constraints, many store procedures, 
lots and lots of structures and rules. Because we have a bunch of different applications and they all need to access this data,
This is a decent, a good role for relational databases, but relational databases are a good guarding against this kind of use case,
they have a fixed schema, they have lots of constraints and relationships and they are very good at enforcing and kicking it back to the app
and go no, you got it wrong, you messed up the data.
So they can be like this strong rock in the middle.
The problem with rocks is they're not very adaptable, they can't be massaged into new and interesting things; a rock is a rock, and it's extremely hard to change.
It's also not a great use case for document databases with their flexibility in schema design, their less enforcement at the database level and more enforcement inside the app.

This is an integration database, and it's generally not a good use case for document databases, if we're still using that this sort of style of document databases, 
it means our queries will be more varied and we probably need to model in a more relational style,less embedded style, just as a rule of thumb.


![alt text](src/pic31.png)

Each one of these little apps is much simpler, it can have its own DB with its own focused query patterns.
When we have an application DB like this, we are more likely to have slightly
more embedded objects because the query patterns are going to be simpler and more focused and more constraints.

**Document patterns**

MongoDB Applied Design Patterns  
https://amzn.to/2qx47oL

Episode#109: MongoDB Applied Design Patterns
https://talkpython.fm/109


#Mapping classes to MongoDB with the ODM MongoEngine

![alt text](src/pic32.png)

Mongoengine is a Document-Object Mapper (think ORM, but for document databases) for working with MongoDB from Python.
It uses a simple declarative API, similar to the Django ORM. 
Documentation available at 
http://docs.mongoengine.org - there is currently a tutorial, a user guide and API reference.

Installing Mongoengine
```
(venv) MacBook-Pro-xxx:mongoDB_basic_syntax xxx$ pip list
Package    Version
---------- -------
pip        10.0.1 
pymongo    3.7.2  
setuptools 39.1.0 
You are using pip version 10.0.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
(venv) MacBook-Pro-xxx:mongoDB_basic_syntax xxx$ pip install mongoengine
Collecting mongoengine
```
Registering connections in mongoengine

In order to use MongoEngine we need to do some configuration of MongoEngine.
Create separate folder in your app (nosql in my case) with connection module called **mongo_setup.py**.
In this module we need to set up the connections with aliases to the application classes. 


```
import mongoengine

def global_init():
    pass
```

In `global_init()` function we need to register the connection. We are not going to open the connection, it doesn't talk to the 
database, but it basically says look if you have a class that maps to a particular type or named part of our application
use this database connection to do the backend work.

```
import mongoengine

def global_init():
    mongoengine.register_connection(alias='core', name='demo_dealership')
    mongoengine.register_connection(alias='analytics', name='demo_dealership_visits')
```

So in our app we can say this class belongs to the core database and this one over here belong to analytics database. 
In production we will pass the extra information we need to use for real server on another port with authentication.

In **service_app.py** file we need to `import mongo_setup` module and define `config_mongo()` method which will run
`mongo_setup.global_init()` 
function inside.

```
import nosql.mongo_setup as mongo_setup

def main():
    print_header()
    config_mongo()
    user_loop()


def print_header():
    print('----------------------------------------------')
    print('|                                             |')
    print('|           SERVICE CENTRAL v.02              |')
    print('|               demo edition                  |')
    print('|                                             |')
    print('----------------------------------------------')
    print()

def config_mongo():
    mongo_setup.global_init()


def user_loop():
    while True:
        ...
     
```

Now we can start defining our classes that we are going to map to the db.
First we need to decide how we are going to store the data and what the data is.

So we are going to have a car, a car is going to have an engine with lots of details about the engine, like its horsepower
and so on. A car is going to have a service history and each entry in the services history is going to be some additional
information, like what was the work performed, how much did it cost, when was it done, etc.

There is going to be an owner who can own multiple cars and a car can be owned by multiple people, so there is a many to
many relationship between owners and cars. The owners have personal information like their address and stuff like that.

We are going to create a file Car in the nosql folder with definition of class for Car object.

We want all the classes, which we want to map to the db, derive from mongoengine.Document. This allows us to load, save 
and query documents. It also provides a field called id, which maps to undescore id in the db. We are going to give it a
couple of pieces of information like what model is it, what make, etc. So we define the properties of document as a descriptor,
so it's a mongoengine. We need also to define the meta dictionary and dictionary is going to say the db alias we want to use is
'core', then we can also control the name of the collections.

nosql/car.py
```
import mongoengine

class Car(mongoengine.Document):
#    id # --> _id = ObjectId()...
    model = mongoengine.StringField()
    make = mongoengine.StringField()
    year = mongoengine.IntField()
    mileage = mongoengine.FloatField()
    vi_number = mongoengine.StringField()

    meta = {
        'db_alias':'core',
        'collection': 'cars',
    }
```

In main application service_app.py we define add_car() function, where we initialize the car object and save it to DB.

service_app.py
```
import nosql.mongo_setup as mongo_setup

from mongoengine.service_central_starter.nosql.car import Car


def main():
    print_header()
    config_mongo()
    user_loop()

...

def add_car():
#    print("TODO: add_car")
    model = input('What is the model?')
    make = input('What is the make?')
    year = int(input('Year built?'))
    mileage = float(input('Mileage?'))
    vin = input('VIN? ')

    car = Car()
    car.model = model
    car.make = make
    car.year = year
    car.mileage = mileage
    car.vi_number = vin

    car.save()   # in order to insert it to db in active record style, where we work with a single document

...

```

We can update the car script with the required fields for the car class.
```
import uuid
import mongoengine


class Car(mongoengine.Document):
#    id # --> _id = ObjectId()...
    model = mongoengine.StringField(required=True)
    make = mongoengine.StringField(required=True)
    year = mongoengine.IntField(required=True)
    mileage = mongoengine.FloatField(default=0.0)
    vi_number = mongoengine.StringField(default=lambda: str(uuid.uuid4()).replace('-',''))

    meta = {
        'db_alias':'core',
        'collection': 'cars',
    }
```

and delete the auto generated variables from add_car() function in main application.


```
def add_car():
    model = input('What is the model?')
    make = input('What is the make?')
    year = int(input('Year built?'))
    # mileage = float(input('Mileage?'))
    # vin = input('VIN? ')

    car = Car()
    car.model = model
    car.make = make
    car.year = year
    # car.mileage = mileage
    # car.vi_number = vin

    car.save()   # in order to insert it to db in active record style, where we work with a single document
```

The next thing we want to look at is the engine and the embedded elements. The engine will equal to a subclass, a class that
represents engines. We define a class Engine in separate file, which will derive from mongoengine as a embedded subdocument.
We will not query and save them independently, we can only work with them through their parent document. 

nosql/engine.py
```
import uuid
import mongoengine

class Engine(mongoengine.EmbeddedDocument):
    horsepower = mongoengine.IntField(required=True)
    liters = mongoengine.FloatField(required=True)
    mpg = mongoengine.FloatField(required=True)
    serial_number = mongoengine.StringField(default=lambda: str(uuid.uuid4()))
```

nosql/car.py

```
import uuid
import mongoengine

from nosql.engine import Engine


class Car(mongoengine.Document):
#    id # --> _id = ObjectId()...
    model = mongoengine.StringField(required=True)
    make = mongoengine.StringField(required=True)
    year = mongoengine.IntField(required=True)
    mileage = mongoengine.FloatField(default=0.0)
    vi_number = mongoengine.StringField(default=lambda: str(uuid.uuid4()).replace('-',''))

   *engine = mongoengine.EmbeddedDocumentField(Engine,required=True)

    meta = {
        'db_alias':'core',
        'collection': 'cars',
    }
```

service_app.py

```
def add_car():
    model = input('What is the model? ')
    make = input('What is the make? ')
    year = int(input('Year built? '))
    # mileage = float(input('Mileage? '))
    # vin = input('VIN? ')

    car = Car()
    car.model = model
    car.make = make
    car.year = year
    # car.mileage = mileage
    # car.vi_number = vin

   *engine = Engine()
   *engine.horsepower = 600
   *engine.mpg = 20
   *engine.liters = 5.0

   *car.engine = engine  # equals to an object

    car.save()   # in order to insert it to db in active record style, where we work with a single document
```

Next we want to add service history to the car document. The question is, do we want to embed this into the car like we 
did it with the engine or save it some other way. Remember, when we are designing our documents one of the primary questions
is in our application do we want that embedded data with us most of the time? In our case, we do almost always want the service
history associated with the car and we don't usually need the service history without the car. We need details about the car 
like the mileage for example. So we probably want to embed the service history as an array into this car. The other thing
we have to care about is that set bounded and is that bound small? The service history should be ongoing, for example once a month.
That would give us at most a hundred of these service histories. Let's say for some reason that like that upper bound is
totally fine with us. It's certainly not crazy unbounded where it's going to escape the 16MB RAM. So we create new class
the servicehistory module with the servicehistory class and save it as an embedded list in the car class.

nosql/servicehistory.py

```
import mongoengine
import datetime

class ServiceHistory(mongoengine.EmbeddedDocument):
    date = mongoengine.DateTimeField(default=datetime.datetime.now) # we pass here a function, we don't want to call it, could use also lambda
    description = mongoengine.StringField()
    price = mongoengine.FloatField()
    customer_rating = mongoengine.IntField(min_value=1,max_value=5)
```
nosql/car.py
```
import uuid
import mongoengine

from nosql.engine import Engine

from nosql.servicehistory import ServiceHistory


class Car(mongoengine.Document):
#    id # --> _id = ObjectId()...
    model = mongoengine.StringField(required=True)
    make = mongoengine.StringField(required=True)
    year = mongoengine.IntField(required=True)
    mileage = mongoengine.FloatField(default=0.0)
    vi_number = mongoengine.StringField(default=lambda: str(uuid.uuid4()).replace('-',''))

    engine = mongoengine.EmbeddedDocumentField(Engine,required=True) # an Embedded Document Field --> single engine, not a list,
   *service_history = mongoengine.EmbeddedDocumentListField(ServiceHistory)

    meta = {
        'db_alias':'core',
        'collection': 'cars',
    }
```

Now it's time to service the car. So, we got a couple of options here, we can grab a random car from db or we can first 
implement the list_cars function, so we could hit list_cars and then we can ask for the id or something to that effect of
the car. We haven't done any queries yet, all we done so far is some inserts. For listing or any sort of query we update 
the list_car function with following object query: `Car.objects().order_by("-year")`

```
def list_cars():
    cars = Car.objects().order_by("-year")
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vi_number, car.year))
    print()
```
```
Available actions:
 * [a]dd car
 * [l]ist cars
 * [f]ind car
 * perform [s]ervice
 * e[x]it

> l
Ferrari -- F40 with vin A3848483F (year 2005)
Audi -- Q5 with vin 1b03ade2b77c4e08b1bb1553603d9543 (year 2012)
BMW -- X6 with vin f9186f802ad144b1a714f5d0e64b8002 (year 2015)
Ferrari -- F40 with vin d5748aa031c6475194aa989ae9518a78 (year 2017)
```

So what we want to do is basically use this vin number, to go find the car we want to service. Now that we can see the cars 
we can say I want to service a car, we can hit s, and it is supposed to say okay what car do you want to service and we give 
it one of these. Then it will go to the database, find the car and then insert a service record to it.

First we update the list_cars function to display details about number of services with prices and some description.

service_app.py
```
def list_cars():
    cars = Car.objects().order_by("-year")
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vi_number, car.year))
       *print("{} of service records".format(len(car.service_history)))
       *for s in car.service_history:
           *print("  * ${:,.02} {}".format(s.price, s.description))
    print()
```

Then we can use the VIN number of car we want to service to filter it out from db.

```
def service_car():
    vin = input("What is the VIN of the car to service? ")
#    car = Car.objects().filter(vi_number=vin).first() # this will return the list of cars that match this
    car = Car.objects(vi_number=vin).first() # simpler version
    if not car:
        print("Car with VIN {} not found!".format(vin))
        return
    print("We will service " + car.model)
```

**Adding service histories by whole document**

Now, let's go and actually add the service record. We are going to import service_history class an create a 
service_history instance in service_car function. Then we are going to ask for the properties of price, service description, 
and customer_rating and append it directly to the car.service_history list as an object. Once we changed the car we need 
to push that to the db.

```
def service_car():
    vin = input("What is the VIN of the car to service? ")
#    car = Car.objects().filter(vi_number=vin).first() # this will return the list of cars that match this
    car = Car.objects(vi_number=vin).first() # simpler version of query, it will give us the same list
    if not car:
        print("Car with VIN {} not found!".format(vin))
        return

    print("We will service " + car.model)
   *service = ServiceHistory()
   *service.price = float(input("What is the price of service? "))
   *service.description = input("What type of service is this? ")
   *service.customer_rating = int(input("How happy is our customer? [1-5] "))

   *car.service_history.append(service)
   *car.save() # to push it to the db
    
```

**Adding service histories  with in-place updates**

We might consider, what will fine for this kind of application, but if there is contention around these documents, like 
multiple things you are trying to update the same record, you could run into some trouble. We could add optimistic
concurrency by manually implementing it and that would solve that problem, but we could actually make this perform better
as well as avoid that problem entirely.

So we are going to ask for a vin, create the service history and instead of pulling the record back, making a change and 
pushing the entire document, which could be like 200K, we just want to move this data over and use `$addToSet` and `$push` 
operators to put it onto the list in the document. In MongoEngine we will use double underscore with operator
`push__service_history=service` to push service ont service history.

```
def service_car():
    vin = input("What is the VIN of the car to service? ")
    service = ServiceHistory()
    service.price = float(input("What is the price of service? "))
    service.description = input("What type of service is this? ")
    service.customer_rating = int(input("How happy is our customer? [1-5] "))

   *updated = Car.objects().filter(vi_number=vin).update_one(push__service_history=service) # it does update the doc, if
    # it finds it, will return 1, if not returns 0.
   *if updated == 0:
        print("Car with VIN {} not found!".format(vin))
        return
```
This is a much higher performance and safer thing to do. We could use also `add_to_set` operator if we want unique elements in 
the list.


**Subdocument queries**

So far we talked about the atomic update operators, but not things like the greater than, less than, exists, doesn't exist,
in set and so on, so we want to look at that, we also want to look at querying into subdocuments. Maybe we want to ask 
questions like show me the cars that have had some really good service or really bad service. We do queries to subarrays with
double underscore as we used it for push onto a thing.

```
def show_poorly_serviced_cars():
    
   *level = int(input("What level of satisfaction are we looking for? [1-5]"))
   *cars = Car.objects().filter(service_history__customer_rating=level)
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vi_number, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * Satisfaction: {} ${:,.0f} {}".format(s.customer_rating, s.price, s.description))
    print()

```

The last thing that we are looking for is, we would like to find the cars that have below excellent service. In PyMongo 
we would write something like this `{ "service_history.customer_rating" : {$lte: level}}`. Here we put query operator at the end
of query statement.

```
def show_poorly_serviced_cars():
    level = int(input("What max level of satisfaction are we looking for? [1-5]"))
    # { "service_history.customer_rating" : {$lte: level}}
   *cars = Car.objects().filter(service_history__customer_rating__lte=level)
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vi_number, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * Satisfaction: {} ${:,.0f} {}".format(s.customer_rating, s.price, s.description))
    print()
```

Sometimes we have to be really careful as we evolve the db, how we are going to deal with the fact that in the database 
there are some documents that has no all properties we later added to the db.  Expecting this is 
really important!  In our case we added vi_number generated by lambda function later to our Car class, after we already 
pushed first car into db. No vi_number in this car. So we need to force of the default of the vin number in there.
```
{
    "_id" : ObjectId("5c0e586abd09bdaf3f9266f8"),
    "model" : "Diablo",
    "make" : "Lamborghini",
    "year" : 2002,
    "mileage" : 0.0,
    "engine" : {
        "horsepower" : 600,
        "liters" : 5.0,
        "mpg" : 20.0,
        "serial_number" : "aed65ac2-69d6-445a-b69d-577127cda160"
    },
    "service_history" : []
}
```
But it is created every time it comes back from the serialization layer, but it doesn't get set from the db, so every time
it goes back, it returns that lambda and gets a new value and we are not saving it. So basically what we need to do is we 
need to upgrade our documents. Sometimes this doesn't matter, but this one where we counted on a default value to be there.


We can write JS script in RoboMongo to update document directly in db or we can write new function in MongoEngine to update
it. We just want it to run one time like a one time upgrade of our documents and if we have a 100 thousand records, probably
fine, if we have billion records this is not how we want to do it. We would better use some kind of in place updater, or 
something better.
```
def update_doc_versions():
    for car in Car.objects():
        car._mark_as_changed('vi_number')
        car.save()
```

**Concept: Registering connections**

![alt text](src/pic33.png)

This work well if we are just connecting on local host, no authentication, default port.. When we get to the production 
deployment, we're going to need ssl, to enable authentication and pass credentials. So we can use a more complicated 
variation here. 

![alt text](src/pic34.png)

The values in data dict for username, password, etc could be in a web app where these values are stored in the config file.

**Concept: Creating basic classes**

![alt text](src/pic35.png)

The way we primarily work with MongoEngine, is we create classes and we map those to collections. So here we have a class
called car and anything that maps to a collection is a top level document that must be derived from mongoengine.document.
Then we set up all the fields that could be simple or as we saw they could be nested rich objects.

![alt text](src/pic36.png)

Finally, we said look, our cars also are going to contain an engine, and we don't want to go and do a separate query to 
a separate table or separate collection specifically to find out details about the engine and store like the car id in the
engine, so instead, we're just going to embed it straight into the car. So we did that by first creating an engine class has 
to derive from mongoengine.EmbeddedDocument and then we're going to set the type of it here to be an embedded document field
which takes two things, the type that we're going to put there so the engine class and whether it's required or optional. 

We also want to store a service_history as a set of rich documents modeled by service records. This time it's a list of them
ant this basically starts out as an empty list and then as we wish we can append these service records to it and then save
them back.

So if we have our car model like this and we put one into the database it's going to come out looking like this:


```
{
    "_id" : ObjectId("5c0ad6d0bd09bd9817b56ac7"),
    "model" : "Q5",
    "make" : "Audi",
    "year" : 2012,
    "mileage" : 0.0,
    "vi_number" : "1b03ade2b77c4e08b1bb1553603d9543",
    "engine" : {
        "horsepower" : 600,
        "liters" : 5.0,
        "mpg" : 20.0,
        "serial_number" : "d7379440-1f08-4c67-9684-3ee0527a6434"
    },
    "service_history" : [ 
        {
            "date" : ISODate("2018-12-09T16:24:18.587Z"),
            "description" : "change of engine",
            "price" : 3000.0,
            "customer_rating" : 5
        }, 
        {
            "date" : ISODate("2018-12-09T16:27:25.065Z"),
            "description" : "flat tire",
            "price" : 120.0,
            "customer_rating" : 4
        }, 
        {
            "date" : ISODate("2018-12-09T19:09:35.549Z"),
            "description" : "waxing",
            "price" : 123.0,
            "customer_rating" : 5
        }, 
        {
            "date" : ISODate("2018-12-09T19:11:38.349Z"),
            "description" : "Checkup",
            "price" : 12.0,
            "customer_rating" : 3
        }
    ]
}

```

**Concept: Inserting objects with mongoengine**

Here we are going to create a car, the car requires the engine and the engine must be an instance of an engine object.  
So we're first going to create an engine, set things like horsepower, the liters, mpg. Then we're going to create the car,
its model is a Bolt, its make is Chevy and the year is 2017, and then we just pass the engine along. So then we have our car,
and right now the id of the car is not stored in the db, so we hit save and boom, now we have a car with its id and its 
default values set all of those things stored in the database. 

![alt text](src/pic37.png)

So this is great for inserting one car, but if you are going to insert a thousand or a hundred thousand or a million cars
you do not want to do this, there's a much better way. You should do some kind of bulk insert but how do you do that? 

Also super easy, let's suppose we have a list of cars that we want to insert and here we are not showing how we initialize 
the cars, but same as above basically, but skip the save step, so we're going to get car one, car two, we want to insert
a bunch of them, we just go car.objects().insert and give it that list and boom it does a bulk insert in MongoDB, which 
if you are inserting many items is much much faster.

![alt text](src/pic38.png)

**Concept: Querying with mongoengine**

![alt text](src/pic39.png)

We might want to query by subdocuments or things contained in a list inside of that document.

![alt text](src/pic40.png)

Here we want to know like show me all the cars that were not rated with great service.

![alt text](src/pic41.png)

**Concept: Updates with mongoengine**

![alt text](src/pic42.png)

When contention is high and we care about performance or we just want to take most advantage of MongoDB, we should use 
the inplace updates. For example here we can see this owner object and this is like the owner of the car, so we want to
record how many times has this owner been to our service shop, owners could own more than one car, so we want to record 
how many times he visited our service.

![alt text](src/pic43.png)


# High performance MongoDB

Simple and fast.

![alt text](src/pic44.png)


![alt text](src/pic45.png)

![alt text](src/pic46.png)

How do we make this fast? Let's have a look at the various knobs, that we can turn to control MongoDB performance.


What levers and knobs do we have?

- Indexes
  
  There are not too many indexes added to MongoDB by default, in fact, the only index that is set up is on _id. Almost 
  always is the problem of incorrect use of indexes.
  
- Document design
  
  It turns out the document design has dramatic implications across the board
   
- Query style
  
  We can write queries differently and end up with higher perfomance results.
  
- Projections and subsets of responses

  We can limit our set of returned responses and this can help for performance


MongoDB being a NoSql database, allows for other types of interactions, other configurations and network topologies, which
we won't cover here.

- Replication (read boost only)
  
  Replication is responsible for redundancy and failover. Instead of just having one server we could have three servers, 
  and they could work in triplicate, one is the primary and you read and write from this db and the other two are just 
  there ready to spring into action, always getting themselves in sync with the primary, and if one goes down, the other
  becomes the primary. There is no performance bnefit from that at all. However, there are ways to configure our connection
  to allow us to read not just from the primary one, but also from the secondary, so we can configure a replication for a 
  performance boost, but mostly this is a durability thing.

- Sharding
  
  The other type of network configuration we can do is what's called sharding. We instead of putting all our data into one 
  individual server, we might spread this across 10 or 20 servers, one 20th of evenly balanced servers, across all of them,
  and then when we issue a query, can either figure out where, if it's based on the shard key, which server to point that at
  and let that one handle the query across the smaller set of data or if it's general like show me all the things with
  greater than this for the price, it might need to query that from all 20 servers, but it would run on parallel on 20 
  machines. So sharding is all about speeding up performance.

**Creating the big DB**

`MacBook-Pro-xxx:etc xxx$ mongorestore --drop --db dealership /Users/xxx/data/dealership `

Source code:

https://github.com/juraj80/mongoDB_with_Python/tree/master/08_perf/starter_big_dealership



New: addition of the concept of an owner class with an embedded list of the owned cars.

nosql/owner.py
```
from datetime import datetime

import mongoengine


class Owner(mongoengine.Document):
    # show off required (not available in mongo or pymongo directly)
    name = mongoengine.StringField(required=True)

    # show off default
    created = mongoengine.DateTimeField(default=datetime.now)

    # allows us to use $set and $inc
    number_of_visits = mongoengine.IntField(default=0)

    # show off many-to-many modeling with one sided list field
    # cars can have multiple owners and an owner can own multiple cares
    car_ids = mongoengine.ListField(mongoengine.ObjectIdField()) # list of ids of the cars, which we push here

    meta = {
        'db_alias': 'core',
        'collection': 'owners',
        'indexes': [
        ]
    }
```

New: all car queries moved to the separate script

services/car_service.py

```
import typing

import bson
import datetime

from nosql.car import Car
from nosql.engine import Engine
from nosql.owner import Owner
from nosql.service_record import ServiceRecord


def create_owner(name: str) -> Owner:
    owner = Owner(name=name)
    owner.save()

    return owner


def create_car(model: str, make: str, year: int,
               horsepower: int, liters: float,
               mpg: float, mileage: int) -> Car:
    engine = Engine(horsepower=horsepower, liters=liters, mpg=mpg)
    car = Car(model=model, make=make, year=year, engine=engine, mileage=mileage)
    car.save()

    return car


def record_visit(customer):
    Owner.objects(name=customer).update_one(inc__number_of_visits=1)


def find_cars_by_make(make) -> Car:
    car = Car.objects(make=make).first()
    return car


def find_owner_by_name(name) -> Owner:
    t0 = datetime.datetime.now()
    owner = Owner.objects(name=name).first()
    dt = datetime.datetime.now() - t0
    print("Owner found in {} ms".format(dt.total_seconds() * 1000))

    return owner


def find_owner_by_id(owner_id) -> Owner:
    owner = Owner.objects(id=owner_id).first()
    return owner


def find_cars_with_bad_service(limit=10) -> typing.List[Car]:
    cars = Car.objects(service_history__customer_rating__lt=4)[:limit]
    return list(cars)


def percent_cars_with_bad_service():
    t0 = datetime.datetime.now()
    bad = Car.objects().filter(service_history__customer_rating__lte=1).count()
    dt = datetime.datetime.now() - t0
    print("bad computed in {} ms, bad: {:,}".format(dt.total_seconds() * 1000, bad))

    all_cars = Car.objects().count()

    percent = 100 * bad / max(all_cars, 1)
    return percent


def find_car_by_id(car_id: bson.ObjectId) -> Car:
    car = Car.objects(id=car_id).first()
    Car.objects().filter(id=car_id).first()
    return car


def add_service_record(car_id, description, price, customer_rating):
    record = ServiceRecord(description=description, price=price, customer_rating=customer_rating)

    res = Car.objects(id=car_id).update_one(push__service_history=record)
    if res != 1:
        raise Exception("No car with id {}".format(car_id))


def add_owner(owner_id, car_id):
    res = Owner.objects(id=owner_id).update_one(add_to_set__car_ids=car_id)
    if res != 1:
        raise Exception("No owner with id {}".format(owner_id))
```

New: script for computing stats

db_stats.py

```

from nosql import mongo_setup
from nosql.car import Car
from nosql.owner import Owner


def main():
    mongo_setup.init()

    print("Computing stats, this WILL take awhile...", flush=True)

    cars = list(Car.objects())
    print("There are {:,} cars.".format(len(cars)))

    owners = list(Owner.objects())
    print("There are {:,} owners.".format(len(owners)))
    owned_cars = sum((len(o.car_ids) for o in owners))
    print("Each owner owns an average of {:.2f} cars.".format(owned_cars / len(owners)))

    service_histories = sum((len(c.service_history) for c in cars))
    print("There are {:,} service histories.".format(service_histories))
    print("Each car has an average of {:.2f} service records.".format(service_histories / len(cars)))


main()
```

New: a script to create a db

Note: a use of Faker to generate random owners

load_data.py

```
import nosql.mongo_setup as mongo_setup
import services.car_service as car_service
from nosql.car import Car
from nosql.engine import Engine
from nosql.owner import Owner

from datetime import datetime
import random
from faker import Faker

from nosql.service_record import ServiceRecord


def main():
    # large data DB example
    car_count = 250_000
    owner_count = 100_000

    # simple DB example
    # car_count = 200
    # owner_count = 100

    mongo_setup.init()
    clear_db()

    t0 = datetime.now()

    fake = create_faker_and_seed()
    owners = create_owners(fake, count=owner_count)
    print("Created {:,.0f} owners".format(len(owners)))
    cars = create_cars(count=car_count)
    print("Created {:,.0f} cars".format(len(cars)))
    if cars and owners:
        add_cars_to_owners(owners, cars)
        create_service_records(cars, fake)

    dt = datetime.now() - t0
    print("Done in {} sec".format(dt.total_seconds()))


models = [
    'Ferrari 488 GTB',
    'Ferrari 360 modena',
    'F430',
    '599 GTB Fiorano',
    '458 Italia',
    'LaFerrari',
    'Testarossa',
    'F12 Berlinetta',
    '308 GTB/GTS',
    'F355',
    'California',
    '575M Maranello',
    'F50',
    'F40',
    'Enzo Ferrari',
]

service_operations = [
    ('Oil change', 200),
    ('New tires', 1000),
    ('New engine', 15000),
    ('Body repair', 4000),
    ('New seat', 5000),
    ('Tune up', 1500),
    ('Air filter', 100),
    ('Flat tire', 200),
]


def create_faker_and_seed():
    fake = Faker()
    fake.seed(42)
    random.seed(42)
    return fake


def clear_db():
    Car.drop_collection()
    Owner.drop_collection()


def create_owners(fake, count=100):
    datetime_start = datetime(year=2000, month=1, day=1)
    datetime_end = datetime(year=datetime.now().year, month=1, day=1)

    owners = []
    print("Building owners")
    for _ in range(0, count):
        owner = Owner()
        owner.name = fake.name()
        owner.created = fake.date_time_between_dates(datetime_start=datetime_start,
                                                     datetime_end=datetime_end,
                                                     tzinfo=None)
        owners.append(owner)

    print("Saving owners")
    Owner.objects().insert(owners, load_bulk=True)

    return list(Owner.objects())


def create_cars(count=200):
    current_car_count = Car.objects().count()
    if current_car_count >= count:
        print("There are currently {:,} cars. Skipping create.")
        return []

    count = count - current_car_count

    hp_factor = 660
    mpg_factor = 21
    liters_factor = 4

    cars = []
    print("Building cars...")
    for _ in range(0, count):
        model = random.choice(models)
        make = 'Ferrari'
        year = random.randint(1985, datetime.now().year)
        mileage = random.randint(0, 150000)

        mpg = int((mpg_factor + mpg_factor * random.random() / 4) * 10) / 10.0
        horsepower = int(hp_factor + hp_factor * random.random() / 2)
        liters = int((liters_factor + liters_factor * random.random() / 2) * 100) / 100.0

        engine = Engine(horsepower=horsepower, liters=liters, mpg=mpg)
        car = Car(model=model, make=make, year=year, engine=engine, mileage=mileage)
        cars.append(car)

    print("Saving cars...")
    Car.objects().insert(cars)

    return list(Car.objects())


def add_cars_to_owners(owners: list, cars: list):
    for o in owners:
        counter = random.randint(0, 5)
        for _ in range(0, counter):
            car = random.choice(cars)
            car_service.add_owner(o.id, car.id)


def create_service_records(cars, fake):
    datetime_start = datetime(year=2000, month=1, day=1)
    datetime_end = datetime(year=datetime.now().year, month=1, day=1)

    for car in cars:
        counter = random.randint(0, 10)
        is_positive = random.randint(0, 1) == 1
        for _ in range(0, counter):
            s = random.choice(service_operations)
            sr = ServiceRecord()
            sr.description = s[0]
            sr.date = fake.date_time_between_dates(datetime_start=datetime_start,
                                                   datetime_end=datetime_end,
                                                   tzinfo=None)
            sr.price = int(s[1] + (random.random() - .5) * s[1] / 4)
            if is_positive:
                sr.customer_rating = random.randint(4, 5)
            else:
                sr.customer_rating = random.randint(1, 3)
            car.service_history.append(sr)
        car.save()


if __name__ == '__main__':
    main()

```

New: how long to take to answer questions from this database

q_and_q.py

```
from nosql.car import Car
from nosql.owner import Owner
from datetime import datetime
import nosql.mongo_setup as mongo_setup


def timed(msg, func):
    t0 = datetime.now()

    func()

    dt = datetime.now() - t0
    print("{} Time: {:,.3f} ms".format(msg, dt.total_seconds() * 1000.0), flush=True)


mongo_setup.init()

print("Time to ask some questions")

timed(
    'How many owners?',
    lambda: Owner.objects().filter().count()
)
timed(
    'How many cars?',
    lambda: Owner.objects().filter().count()
)

timed(
    'Find the 10,000th owner?',
    lambda: Owner.objects().order_by('name')[10000:10001][0]
)

owner = Owner.objects().order_by('name')[10000:10001][0]


def find_cars_by_owner(owner_id):
    the_owner = Owner.objects(id=owner_id).first()
    cars = Car.objects().filter(id__in=the_owner.car_ids)
    return list(cars)


timed(
    'How many cars are owned by the 10,000th owner?',
    lambda: find_cars_by_owner(owner.id)
)


def find_owners_by_car(car_id):
    owners = Owner.objects(car_ids=car_id)
    return list(owners)


car = Car.objects()[10000:10001][0]
timed(
    'How many owners own the 10,000th car?',
    lambda: find_owners_by_car(car.id)
)

owner50k = Owner.objects()[50000:50001][0]
timed(
    'Find owner 50,000 by name?',
    lambda: Owner.objects(name=owner50k.name).first()
)

timed(
    'Cars with expensive service?',
    lambda: Car.objects(service_history__price__gt=16800).count()
)

timed(
    'Cars with expensive service and spark plugs?',
    lambda: Car.objects(service_history__price__gt=16800, service_history__description='Spark plugs').count()
)

timed(
    'Load cars with expensive service and spark plugs?',
    lambda: list(Car.objects(service_history__price__gt=16800, service_history__description='Spark plugs'))
)

timed(
    'Load car name and ids with expensive service and spark plugs?',
    lambda: list(Car.objects(service_history__price__gt=16800, service_history__description='Spark plugs')
                 .only('make', 'model', 'id'))
)

timed(
    'Highly rated, high price service events?',
    lambda: Car.objects(service_history__customer_rating=5, service_history__price__gt=16800).count()
)

timed(
    'Low rated, low price service events?',
    lambda: Car.objects(service_history__customer_rating=1, service_history__price__lt=50).count()
)

timed(
    'How many high mileage cars?',
    lambda: Car.objects(mileage__gt=140000).count()
)
```

Query: Find a 61006th car and find all the owners

![alt text](src/pic47.png)

Query: Find a car with a service price higher than 16800.

`db.cars.find({'service_history.price':{$gt: 16800}})`

0.705 sec.

Why is this taking 700 milliseconds?

`db.cars.find({'service_history.price':{$gt: 16800}}).explain()`

```
/* 1 */
{
    "queryPlanner" : {
        "plannerVersion" : 1,
        "namespace" : "dealership.cars",
        "indexFilterSet" : false,
        "parsedQuery" : {
            "service_history.price" : {
                "$gt" : 16800.0
            }
        },
        "winningPlan" : {
            "stage" : "COLLSCAN",  <-- NOT GOOD
            "filter" : {
                "service_history.price" : {
                    "$gt" : 16800.0
                }
            },
            "direction" : "forward"
        },
        "rejectedPlans" : []
    },
    "serverInfo" : {
        "host" : "xxx.local",
        "port" : 27017,
        "version" : "4.0.4",
        "gitVersion" : "f288a3bdf201007f3693c58e140056adf8b04839"
    },
    "ok" : 1.0
}
```

Python code with mongoengine:

Without indexes

`mongoDB_basic_syntax/08_perf/starter_big_dealership/q_and_a.py
`
```
Time to ask some questions
How many owners? Time: 40.521 ms
How many cars? Time: 0.941 ms
Find the 10,000th owner? Time: 1,911.872 ms
How many cars are owned by the 10,000th owner? Time: 58.604 ms
How many owners own the 10,000th car? Time: 1.352 ms
Find owner 50,000 by name? Time: 22.854 ms
Cars with expensive service? Time: 17.106 ms
Cars with expensive service and spark plugs? Time: 993.791 ms
Load cars with expensive service and spark plugs? Time: 20.993 ms
Load car name and ids with expensive service and spark plugs? Time: 21.479 ms
Highly rated, high price service events? Time: 21.930 ms
Low rated, low price service events? Time: 3.592 ms
How many high mileage cars? Time: 956.467 ms

Process finished with exit code 0
```

**Adding indexes via the shell**

`db.cars.createIndex({'service_history.price':1 }, {name: 'Search by service history price'})
`

```
{
    "createdCollectionAutomatically" : false,
    "numIndexesBefore" : 1,
    "numIndexesAfter" : 2,
    "ok" : 1.0
}
```

Running a query agian.

![alt text](src/pic48.png)

Response is now 5 milliseconds.

`db.cars.find({'service_history.price':{$gt: 16800}}).explain()`

```
/* 1 */
{
    "queryPlanner" : {
        "plannerVersion" : 1,
        "namespace" : "dealership.cars",
        "indexFilterSet" : false,
        "parsedQuery" : {
            "service_history.price" : {
                "$gt" : 16800.0
            }
        },
        "winningPlan" : {
            "stage" : "FETCH",
            "inputStage" : {
                "stage" : "IXSCAN",  <-- WINNING PLAN IS INDEX SCAN, WHICH IS SO MUCH FASTER
                "keyPattern" : {
                    "service_history.price" : 1.0
                },
                "indexName" : "Search by service history price",
                "isMultiKey" : true,
                "multiKeyPaths" : {
                    "service_history.price" : [ 
                        "service_history"
                    ]
                },
                "isUnique" : false,
                "isSparse" : false,
                "isPartial" : false,
                "indexVersion" : 2,
                "direction" : "forward",
                "indexBounds" : {
                    "service_history.price" : [ 
                        "(16800.0, inf.0]"
                    ]
                }
            }
        },
        "rejectedPlans" : []
    },
    "serverInfo" : {
        "host" : "xxx.local",
        "port" : 27017,
        "version" : "4.0.4",
        "gitVersion" : "f288a3bdf201007f3693c58e140056adf8b04839"
    },
    "ok" : 1.0
}
```
Python code with mongoengine:

With indexes

`mongoDB_basic_syntax/08_perf/starter_big_dealership/q_and_a.py
`
```
Time to ask some questions
How many owners? Time: 5.327 ms
How many cars? Time: 0.597 ms
Find the 10,000th owner? Time: 372.768 ms
How many cars are owned by the 10,000th owner? Time: 3.495 ms
How many owners own the 10,000th car? Time: 0.606 ms
Find owner 50,000 by name? Time: 22.367 ms
Cars with expensive service? Time: 2.480 ms
Cars with expensive service and spark plugs? Time: 19.903 ms
Load cars with expensive service and spark plugs? Time: 18.960 ms
Load car name and ids with expensive service and spark plugs? Time: 19.858 ms
Highly rated, high price service events? Time: 16.848 ms
Low rated, low price service events? Time: 0.878 ms
How many high mileage cars? Time: 142.728 ms

Process finished with exit code 0

```

**Adding indexes in mongoengine**

By doing this in MongoEngine and pushing our code into production will ensure that the database has all the right indexes
set up for to operate correctly. This way all the indexes that are required will be there. Anytime we want to do a filter by,
a greater than, an equality, or we want to do a sort, we need an index. Let's go to the owner class and let's add the ability
to sort it by name or equivalently also do a filter like find exactly by name.


Query: Find the 10,000th owner by name?
```
timed(
    'Find the 10,000th owner by name?',
    lambda: Owner.objects().order_by('name')[10000:10001][0]
)
```
Response: 

`Find the 10,000th owner by name? Time: 295.879 ms`

Too long. It's the sorting problem that we are running into.

`db.cars.find({}).sort({'name':1}).explain()`

winningPlan:

` "stage" : "COLLSCAN",`


So let's go to the owner class and add the ability to sort it by name, equivalently do a filter like find exactly by name.



owner.py

```
from datetime import datetime

import mongoengine

class Owner(mongoengine.Document):
    # show off required (not available in mongo or pymongo directly)
    name = mongoengine.StringField(required=True)

    # show off default
    created = mongoengine.DateTimeField(default=datetime.now)

    # allows us to use $set and $inc
    number_of_visits = mongoengine.IntField(default=0)

    # show off many-to-many modeling with one sided list field
    # cars can have multiple owners and an owner can own multiple cares
    car_ids = mongoengine.ListField(mongoengine.ObjectIdField()) # list of ids of the cars, which we push here

    meta = {
        'db_alias': 'core',
        'collection': 'owners',
    *   'indexes': [
    *       'name',  
    *   ]
    }
```
Query: How many cars are owned by the 10,000th owner? Time: 3.615 ms

```
owner = Owner.objects().order_by('name')[10000:10001][0]


def find_cars_by_owner(owner_id):
    the_owner = Owner.objects(id=owner_id).first()
    cars = Car.objects().filter(id__in=the_owner.car_ids) #id is in a set
    return list(cars)


timed(
    'How many cars are owned by the 10,000th owner?',
    lambda: find_cars_by_owner(owner.id)
)

```
We're doing two queries, but both of them are hitting the id thing, so those should both be indexed, because ids are 
always indexed, that's why 3 milliseconds.

Query: How many owners own the 10,000th car? Time: 68.941 ms

```
def find_owners_by_car(car_id):
    owners = Owner.objects(car_ids=car_id)
    return list(owners)


car = Car.objects()[10000:10001][0]
timed(
    'How many owners own the 10,000th car?',
    lambda: find_owners_by_car(car.id)
)
```
in the shell:

`db.owners.find({car_ids: ObjectId('5928f6343ae7407d71754b80')}).explain()
`

winningPlan:

` "stage" : "COLLSCAN",`

We want to have an index on car ids, so we must add it to the owner class.

```
 meta = {
        'db_alias': 'core',
        'collection': 'owners',
        'indexes': [
            'name', 'car_ids'
        ]
    }
```

Response:

`How many owners own the 10,000th car? Time: 2.689 ms`

Query: Cars with expensive service? Time: 712.874 ms
```
timed(
    'Cars with expensive service?',
    lambda: Car.objects(service_history__price__gt=16800).count()
)
```
Here we are looking at the service history and then we're navigating that hierarchy with double underscore, going to the
price. So let's add indexes to the car class with 'service_history.price' as an index.

car.py
```
meta = {
        'db_alias': 'core',
        'collection': 'cars',
        'indexes': [
            'service_history.price',
        ]
    }
```
Response: 

`Cars with expensive service? Time: 5.623 ms`


Query: Cars with expensive service and spark plugs? Time: 28.307 ms
```
timed(
    'Cars with expensive service and spark plugs?',
    lambda: Car.objects(service_history__price__gt=16800, service_history__description='Spark plugs').count()
)
```
Response:

`Cars with expensive service and spark plugs? Time: 6.436 ms
`

in the shell:

`db.cars.find({'service_history.price':{$gt:16800}}, {'service_history.description':'Spark plugs'}).explain()`

winningPlan:

` "stage" : "COLLSCAN",`

We need to add 'service_history.description' to car indexes.
```
   meta = {
        'db_alias': 'core',
        'collection': 'cars',
        'indexes': [
            'service_history.price',
            'service_history.description'
        ]
    }
```

Response:

`Load cars with expensive service and spark plugs? Time: 1.770 ms
`

But what would be even better is if we could do the description and the price as a single thing. How can we do that?
We can actually create a composite index in car indexes like this:
```
meta = {
        'db_alias': 'core',
        'collection': 'cars',
        'indexes': [
            'service_history.price',
            'service_history.description',
            {'fields':['service_history.price', 'service_history.description']}
        ]
    }
```

Response:

`Cars with expensive service and spark plugs? Time: 0.676 ms`

We added one index, and then we added the description index, it turns out that was a better index, and finally we added 
composite index, and we took it to half a millisecond. We did count function, it's basically having the database do all 
the work, but there's zero serialization.
    
Query: Load cars with expensive service and spark plugs? Time: 0.706 ms
```
timed(
    'Load cars with expensive service and spark plugs?',
    lambda: list(Car.objects(service_history__price__gt=16800, service_history__description='Spark plugs'))
)
```
Here we calling a list, so we are deserializing, we're actually pulling all of those records back. Let's check this query:

`db.cars.find({'service_history.price':{$gt:15000}}).count()`

65264 cars had 15 thousand dollar service or higher, after all this is a Ferrari dealership :)
It turns out it's a really bad idea to pull back that many cars, so let's limit that to just a thousand cars.

```
timed(                                                                   
    'Load cars with expensive service and spark plugs?',                 
    lambda: list(Car.objects(service_history__price__gt=15000)[:1000])   
)                                                                        
                                                                         
timed(                                                                   
    'Load car name and ids with expensive service and spark plugs?',     
    lambda: list(Car.objects(service_history__price__gt=15000)           
                  .only('make', 'model', 'id')[:1000])                   
 )   
```                                                                    

Response:
```
Load cars with expensive service and spark plugs? Time: 1,068.853 ms
Load car name and ids with expensive service and spark plugs? Time: 166.072 ms
```
In second query we are using `.only()` function, it says don't pull back the other things, just give me these three fields
when you create them. It makes it basically ten times faster. It turns out that the deserialization step in MongoEngine is 
a little bit expensive so if we want a million cars into that list, it's going to take a little bit.

Query: 

Highly rated, high price service events? Time: 16.899 ms
Low rated, low price service events? Time: 1.061 ms

```
timed(                                                                                                   
    'Highly rated, high price service events?',                                                          
    lambda: Car.objects(service_history__customer_rating=5, service_history__price__gt=16800).count()    
) 

timed(                                                                                                 
    'Low rated, low price service events?',                                                            
    lambda: Car.objects(service_history__customer_rating=1, service_history__price__lt=50).count()     
)                                                                                                                                                                                                             
```   
We don't have customer_rating between indexes, so we add it to the car indexes to speed the query up.

       meta = {
        'db_alias': 'core',
        'collection': 'cars',
        'indexes': [
            'service_history.price',
           *'service_history.customer_rating',
            'service_history.description',
            {'fields':['service_history.price', 'service_history.description']},
           *{'fields':['service_history.price', 'service_history.customer_rating']}
            
        ]
    }
       
Response:

Highly rated, high price service events? Time: 19.476 ms
Low rated, low price service events? Time: 0.894 ms

Query: How many high mileage cars? Time: 163.711 ms
```
timed(                                                            
    'How many high mileage cars?',                                
    lambda: Car.objects(mileage__gt=140000).count()               
)                                                                 
```  

We need to add the mileage field between indexes to speed query up. 
```
 meta = {
        'db_alias': 'core',
        'collection': 'cars',
        'indexes': [
           *'mileage',
            'service_history.price',
            'service_history.customer_rating',
            'service_history.description',
            {'fields':['service_history.price', 'service_history.description']},
            {'fields':['service_history.price', 'service_history.customer_rating']}
        ]
    }                                                            
```    

Response:
`
How many high mileage cars? Time: 5.176 ms
`

So we can add three types of indexes with MongoEngine:
- flat indexes (plain fields)
- nested indexes 
- composite indexes   

How do we know that we are done with this performance adjustments?
We know we are done when all of these numbers come by and they're all within reason of what we're willing to take.  

In real application we want to set up profiling

https://docs.mongodb.com/manual/tutorial/manage-the-database-profiler/

`db.setProfilingLevel() 
`
It will generate a table called system.profile with small queries.
We can go there and see what queries are slow, clear it out, run your app, see what shows up in there, add a bunch of
indexes, make them fast, clear that table, then turn around and run your app again. Or we can find the slowest one, make 
it faster, clear out the profile and just iterate that process. 

**Concept: Indexes via shell** 

Creating these indexes is even more important in document databases than it is in relational dbs.

![alt text](src/pic49.png)

**Concept: Indexes via mongoengine** 

We don't have to go to the shell and manually type all the indexes, we basically go to each individual top level document,
so all the things that derive from mongoengine.document, not the embedded documents, and we go to the meta section and we
add an indexes, basically array.

![alt text](src/pic50.png)

**Concept: Document design for performance** 

One of the most important things we can do for performance in our db and these document dbs is think about our document
design.

Important questions to consider:

Should we embed stuff, should we not, what embeds where, do we embed just ids, do we embed the whole thing.

![alt text](src/pic51.png)

We should use performance profiling and tuning to figure out where we might use `only()` keyword.

We should also consider what is the right size of document.

`db.getCollection('cars').stats()` - it will return statistics about the document.

The most important info is about average object size, 700 bytes, fine for our db.

![alt text](src/pic52.png)

**Concept: Projections** 

One of the last simple tools we have is the ability to restrict the data returned from the document

![alt text](src/pic53.png)

#Deploying MongoDB in production (and playing it safe)

Problem is that MongoDB listen on the wide open internet without a username and password and without encryption by the 
default.

![alt text](src/pic54.png)

![alt text](src/pic55.png)

**Creating couple of web servers**

![alt text](src/pic56.png)

We're going to create two servers through Digital Ocean, one that's going to be our web server that's going to be our web server and the one that
is the deployment production server.

https://cloud.digitalocean.com 


1.Create a Droplet
2.Choose a Distribution
3.Choose size
4.Choose a datacenter region
5.Select additional options - monitoring
6.Add your SSH keys - new or existing SSH key
7.Choose a hostname - themongoserver


**Generating SSH keys on Mac OSX**

`man ssh-keygen   
`
It will give us all the parameters

`ssh-keygen -t rsa -b 2048
`
When we want to upload a public key, we can just copy the text from .pub file

`more publickey.pub
`

Try connection to the remote root:
`
ssh root@ip_of_remote_server
 `
 
`ssh -i /path_to_privatekey root@ip_of_remote_server
`

If denied, register your ssh to your user:

`ssh-add -K ~/.ssh/*.key
`

If connected, _check for updates_ `apt update`

To _upgrade_ server `apt upgrade`

To _logout_ from root type `exit`
To _restart_ the system type `reboot`


With same steps create second cloud server for the fake web app with the name: thewebserver

Try connection to the remote root:
`
ssh root@ip_of_remote_server
`

**Install MongoDB for production use**

MongoDB has the service called MongoDB Atlas, which is database as a service, where you have to create a AWS account,
EC2 account, you give them access to make machines and manage those machines on your behalf and they can create a replica
sets and other stuff. This is a service that manages your EC2 machines upon your behalf.

Other option is mLab free Sandbox or Shared one for light production work, so you can go and just get MongoDB as a service.

But we want to know how to create our onw MongoDB servers.

If we try to connect directly to the themongoserver without knowing IP we get:

`MacBook-Pro-xxx:.ssh xxx$ ssh root@thewebserver
ssh: Could not resolve hostname thewebserver: nodename nor servname provided, or not known
`
Let's associate the IP of the remote servers with its domain name save both to the /etc/hosts file.

`sudo nano /etc/hosts`

```
165.227.175.56 thewebserver
138.68.104.69 themongoserver
```

Now we can try connect with `root@themongoserver` or `root@thewebserver`.

Connect to the themongoserver and install MongoDB according the following steps: 

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

1. Import the public key used by the package management system.

`sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
`

2. Create a list file for MongoDB for the proper version of Ubuntu (16.04 in our case).

`echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
`

3. Reload local package database

`
sudo apt-get update
`

4. Install the latest stable version of MongoDB.

`apt install mongodb-org`

The MongoDB is now installed on our cloud server and next time we run apt update and then upgrade that could potentially 
install next version of mongo.

To run the MongoDB service:

`service mongod start
`

We can ask status:

`service mongod status
` 

To connect to MongoDB:

`mongo`


**Concept: Installing MongoDB for production**

![alt text](src/pic57.png)


**Limit your network exposure**

One of the most important things we can do to make our MongoDB server safe, even if we screw up the configuration, the 
authentication, the encryption, is to make sure nobody can talk to it. So we're going to do two simple things right away
to lock down our server. Obviously our web app should be able to talk to it and it's this probably within a data center we 
could possibly get to it from our local machines, but we will do things like ssl tunnels and so on to do that, so we won't
open up any extra ports for this. However, there's always something out there lurking, things that would love to talk to 
server on port 27017, the default port, or maybe 1.8 or 1.9, or 20, depending on the service you're running. So we want to 
block those requests with the firewall and couple of other things.

![alt text](src/pic58.png)

On your webserver install mongodb shell:

`root@thewebserver:~# apt install mongodb-org-shell
`

On your mongoserver:

`root@themongoserver:~# more/etc/mongod.conf
`

Your mongoserver is listening only on local host, so before changing it, first we would like to make it safe, we don't
want to just listen on the open internet right away, so let's first block access to all of the ports and everything
basically except for initially ssh, so what we're going to use is something built into Ubuntu called uncomplicated 
firewall. 

First block all the ports:

`root@themongoserver:~# ufw default deny incoming
`

Then allow our server to get back out:

`root@themongoserver:~# ufw default allow outgoing
`

Allow ssh back to this server:

`root@themongoserver:~# ufw allow ssh
`

Ask for status:

`root@themongoserver:~# ufw status
`

Enable the default firewall:

`root@themongoserver:~# ufw enable
`

So now nothing can talk to any port except for 22 ssh at all on this server. The one final thing to do is to ping the
web server.


`root@themongoserver:~# ping thewebserver
`

The next we want is to allow the web server to get to the Mongo server.

`root@themongoserver:~# ufw allow from ip_of_thewebserver to any port 10001
`

The port 27017 is the default port and running MongoDB on the default port is probably a stupid idea. Everyone is scanning
the wide open internet for 27017. So even though we think our firewalls are blocking the wide open internet for everything
except for ssh, let's go ahead and change the port. So we're going to say 10001 is the port we're going to run Mongo.

So our server is running and listening on that port. 

And the next thing to do is to change the port in config file:

`root@themongoserver:~# nano /etc/mongod.conf
`
```
# network interfaces
net:
  port: 10001
  bindIp: 127.0.0.1
  ```
 
Now restart the MongoDb service:

`root@themongoserver:~# service mongod restart
`

Connect to mongo on new port:

`root@themongoserver:~# mongo --port 10001
`

But it's still not going to listen to us on webserver:

`root@thewebserver:~# mongo --host ip_of_themongoserver
`

`exception: connect failed
`

The reason is that on the webserver we are still not listening on the public internet, we're just listening on local host.
So let's change it.

```
root@thewebserver:~# ufw default deny incoming
root@thewebserver:~# ufw default allow outgoing
root@thewebserver:~# ufw allow ssh
root@thewebserver:~# ufw allow 80
root@thewebserver:~# ufw allow 443
root@thewebserver:~# ufw enable
```

So now we've got the webserver sort of foul lock down just to play along and can talk to the mongo server, but mongoserver
is still not listening. We don't want to make it listen, until we go through a few other steps - encryption of the connection,
which within the same data center maybe doesn't matter, but we're going to add it anyway and authentication.

![alt text](src/pic59.png)

**Adding encrypted communication for MongoDB**

https://docs.mongodb.com/manual/tutorial/configure-ssl/

For our mongoDB server we want to add communication level encryption, basically ssl. Now we could go get a proper ssl 
certificate, we could even use let's encrypt, but because this is only talked to from our few servers we can actually just
do an autogenerated one, so a self signed certificate.

```
root@themongoserver:~# cd /etc/ssl
root@themongoserver:/etc/ssl# ls
root@themongoserver:/etc/ssl# openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes -out mongodb-cert.crt -keyout mongodb-cert.key
root@themongoserver:/etc/ssl# ls
```

Now when we have a private and public keys, the next thing is to generate a pem file, which is really just the combination
of the public and private key and we can do it with a `cat` command like this.

```
root@themongoserver:/etc/ssl# cat mongodb-cert.key mongodb-cert.crt > mongodb.pem
root@themongoserver:/etc/ssl# more mongodb.pem
```

Now we've got the private key and the certificate there. The next thing to do is actually tell MongoDB, hey, I would like 
you to use encryption and I would like to use this particular key.

`root@themongoserver:/etc/ssl# nano /etc/mongod.conf
`

We want to go to network interfaces and add a ssl information.

```
# network interfaces
net:
  port: 10001
  bindIp: 127.0.0.1
  ssl:
     mode: requireSSL
     PEMKeyFile: /etc/ssl/mongodb.pem
  ```

Then we just have to restart mongo:

`root@themongoserver:/etc/ssl# service mongod restart`

Note: If something goes wrong try to get status and then check the log file:

`root@themongoserver:/etc/ssl# service mongod status`

`root@themongoserver:/etc/ssl# more /var/log/mongodb/mongod.log`

To connect to MongoDB:

`root@themongoserver:/etc/ssl# mongo --port 10001`

If `Error: network error while attempting to run command 'isMaster' on host '127.0.0.1:10001'`

Run:

`root@themongoserver:/etc/ssl# mongo --port 10001 --sslAllowInvalidCertificates --ssl`

Now we are talking to the server on its non default port using its non valid ssl certificate.

The final thing is to change bindIp in network interfaces to 0000 which allow our web app to talk.

`root@themongoserver:/etc/ssl# nano /etc/mongod.conf
`

```
# network interfaces
net:
  port: 10001
  bindIp: 0.0.0.0
  ssl:
     mode: requireSSL
     PEMKeyFile: /etc/ssl/mongodb.pem
  ```

We have the encryption of a communication that's good, but not good enough. What we need to be able to do is to restrict
this to only people with username and password and because we're doing this over ssl that password exchange is relatively
safe.

**Concept: Adding encrypted communication for MongoDB**

![alt text](src/pic60.png)

This was an important step to enabling ssl and secure communication on our MongoDB server.


**Adding authentication to MongoDB**

So we've encrypted our MongoDB, we've got it hidden behind a firewall and listening on a non standard port, let's add an
authentication.

`root@themongoserver:/etc/ssl# mongo --port 10001 --sslAllowInvalidCertificates --ssl`

Notice there is no username or password required to get into the db.
First thing to do is we're going to run this db.create user command. We want to create a user to admin entire database server.

```
> use admin
switched to db admin
> db
admin
> show collections
system.version
```

Now we can run this db command to create users against admin which means kind of global.

_db.createUser( { user: "the_db_admin", pwd: "the-pw", roles: ["userAdminAnyDatabase", "readWriteAnyDatabase", "dbAdminAnyDatabase", "clusterAdmin"] } )_

To create strong password for db_admin lets use ptpython:

```
MacBook-Pro-xxx:~ xxx$ pip install ptpython
MacBook-Pro-xxx:~ xxx$ ptpython

>>> import uuid                                                                                                                                                    

>>> print("the-password-{}".format(uuid.uuid4()))                                                                                                                  
the-password-16de3b03-8504-44f9-9505-af1dc70436c4
```

So now we have user: "the_db_admin", pwd: the-password-..., we have to specify the roles,
we could create multiple users, that have certain restricted access to different databases, but for this case we're just 
going to say this user the_db_admin can admin, readWrite databases or clusters. Just because you are an admin for a db, 
does not mean you can read and write to it, you could just create users and things like that, so you need them all.

`> db.createUser( { user: "the_db_admin", pwd: "the-password-16de3b03-8504-44f9-9505-af1dc70436c4", roles: ["userAdminAnyDatabase", "readWriteAnyDatabase", "dbAdminAnyDatabase", "clusterAdmin"] } )
`

Next we go to the mongo config file and add a security information.

`root@themongoserver:/etc/ssl# nano /etc/mongod.conf
`
```
security:
  authorization: enabled

```

Save and restart the mongo service and check status:

```
root@themongoserver:/etc/ssl# service mongod restart

root@themongoserver:/etc/ssl# service mongod status

```

If we try to connect to MongoDB, now it will connect:

`root@themongoserver:/etc/ssl# mongo --port 10001 --sslAllowInvalidCertificates --ssl`

but it will not allow you to see the dbs. You have to use your admin name and password:
```
> show dbs
2018-12-19T18:55:05.325+0000 E QUERY    [js] Error: listDatabases failed:{
	"ok" : 0,
	"errmsg" : "command listDatabases requires authentication",
	"code" : 13,
	"codeName" : "Unauthorized"
}

> use admin
switched to db admin
> db.auth({user: "the_db_admin", pwd: "the-password-16de3b03-8504-44f9-9505-af1dc70436c4" })
1
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
```

But we would probably want to do it shorter way:

`root@themongoserver:~# mongo --port 10001 --sslAllowInvalidCertificates --ssl -u the_db_admin -p the-password-16de3b03-8504-44f9-9505-af1dc70436c4 --authenticationDatabase admin
`
```
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
```

**Concept: Adding authentication to MongoDB**

![alt text](src/pic61.png)

At this point, we have set up our MongoDB in a safe way, check the config file if your network is properly set. The final thing that we might consider and it depends on how you
want to run your database, you might set up a replica set to have failover and multi machine redundancy. That's certainly
a next step you could take, so check out the docs.


**The BIG moment**

1.Connect to the webserver:

`ssh root@thewebserver
`

2. From the webserver connect to the mongo server using the mongo server IP and admin username and password.

`root@thewebserver:~# mongo --port 10001 --host 138.68.104.69 --sslAllowInvalidCertificates --ssl -u the_db_admin -p the-password-16de3b03-8504-44f9-9505-af1dc70436c4 --authenticationDatabase admin`

Notes:

Only thewebserver could connect to themongoserver, other request will time out.
We have to pass the username and the password (in the auth string) if not we can still connect to the server but nothing will work

Let's do one more thing, let's install the glances app on themongoserver.

`root@themongoserver:~# apt install glances
`

It's a really cool way to look at our server, we can see how much memory and CPU is our db using. Type m for sorting by memory,
type c for CPU.

Note: if you install pip3 and then glances via pip3 you get a much nicer version of glances

```
sudo apt-get -y install python3-pip

pip3 install glances

glances
```

![alt text](src/pic62.png)


**Connecting to MongoDB via Python**

Let's go back to our service_app template file and set the global_init function up for running it in our production environment.
If we would put the template on our web server, it would talk to local host and have a big fail. So instead we need to go and
add some default parameters to our mongo connection in mongo_setup.py.

nosql/mongo_setup.py

```
import mongoengine

* def global_init(user=None, password=None, port=27017, server='localhost', use_ssl=True):
*    if user or password:
*        pass
*    else:
*        print("--> Registering dev connection")
        mongoengine.register_connection(alias='core', name='demo_dealership')
```

We're going to create a dictionary, where we set all of its keys to the global_init keyword arguments. 

```
import ssl
import mongoengine


def global_init(user=None, password=None, port=27017, server='localhost', use_ssl=True):
    if user or password:
        data = dict(
            username=user,
            password=password,
            host=server,
            port=port,
            authentication_source='admin',
            authentication_mechanism='SRAM-SHA-1',
            ssl=use_ssl,
            ssl_cert_regs=ssl.CERT_NONE) # ignore a self sign certificate
        mongoengine.register_connection(alias='core', name='demo_dealership', **data)
        data['password'] = '************'
        print("--> Registering prod connection: {}".format(data))
    else:
        print("--> Registering dev connection")
        mongoengine.register_connection(alias='core', name='demo_dealership')
```
The next thing we need to go our service app where we calling the global_init function and pass all the details required 
for the connection.

service_app.py
```
def config_mongo():
    mongo_setup.global_init(
        'the_db_admin',
        'the-password-16de3b03-8504-44f9-9505-af1dc70436c4',
        10001,
        '165.227.175.56'
        )
```  
Now if we run this, it will probably going to timeout. We already saw we can't connect to the server, so we need to push
this up to the git repository and clone it to the webserver.

1. First push your deployment files to the git and then clone them on your webserver.
2. Then create and activate virtual env on the webservet in order to pip install of mongoengine package.
3. Install mongoengine package
4. Finally run the service_app.py file within your env

``` 
root@thewebserver:~/service-deploy# apt-get install python3-venv
root@thewebserver:~# python3 -m venv ~/sample_env
root@thewebserver:~# source ~/sample_env/bin/activate
(sample_env) root@thewebserver:~# pip install mongoengine
(sample_env) root@thewebserver:~# python3 ./service-deploy/service_app.py
```  
      
_Note: Useful basic shell commands_

To make a directory

`mkdir ~/mydir
`

To remove a directory that contains other files or directories with a prompt for approval to delete each of the files.

`rm -r mydir
`

If we don't want to receive a prompt for each file.

`rm -rf mydir
`

To copy (-r copy recursively) a directory to a new location:

`cp -r /path/to/directory /path/to/location/new-name
`

**Concept: Connecting to MongoDB via Python**

Let's review how we connected to the mongo on our local machine:

![alt text](src/pic63.png)


For connection to a real web server, we are going to use a more advanced version:

![alt text](src/pic64.png)


**MongoDB admin tools**

It's great that we have our MongoDB running in production. We've got our web server and a MongoDB server and they're 
entirely locked down. If we tried to connect to that Mongo server, even though it's on a different port with ssl and 
authentication, we couldn't talk to it because the Ubuntu firewall was blocking access from everywhere in the world
except for that one fake web server. So we can't talk to it, we can't manage it with Robomongo, which would be great, but
we can't even connect to it via the shell. We tried that and it failed. 

But we can ssh into the Mongo server with `ssh root@themongoserver` and switch to db admin but that's it, nothing more. 

It turns out we can set up an ssh tunnel using that mechanism. If we run this command ( -f to run in the background,
ssh to the root@themongoserver, -L map the local port 10001 on the remote machine called the localhost 10001) it creates 
a background task of ssh tunneling one port locally over that server port.

`ssh -f root@themongoserver -L 10001:localhost:10001 -N
`

Now if we try this, we will have access to the db.

`mongo --port 10001 --sslAllowInvalidCertificates --ssl -u the_db_admin -p the-password-16de3b03-8504-44f9-9505-af1dc70436c4 --authenticationDatabase admin
`
Notice there's no host there, we have the port 10001, what is the host if we don't specify one - local host, but local host
10001 really means the Mongo server 10001.

```
> db.serverStatus()
{
	"host" : "themongoserver:10001",
	"version" : "4.0.4",
	"process" : "mongod",
...
```

We can even connect with the Robomongo:

![alt text](src/pic65.png)
![alt text](src/pic66.png)
![alt text](src/pic67.png)
![alt text](src/pic68.png)

Now when we've connected with Robomongo we can for example add an index for service_history.price.

![alt text](src/pic69.png)
![alt text](src/pic70.png)
![alt text](src/pic71.png)

Last thing we will see, is how to do a backup of a database using the mongodump function.

Let's go to our desktop and make a dir called the backtest where we mongodump our db.

```
MacBook-Pro-xxx:~ xxx$ cd Desktop
MacBook-Pro-xxx:Desktop xxx$ mkdir backtest
MacBook-Pro-xxx:Desktop xxx$ cd backtest
MacBook-Pro-xxx:backtest xxx$ mongodump --help
MacBook-Pro-xxx:backtest xxx$ mongodump --port 10001 --sslAllowInvalidCertificates --ssl -u the_db_admin -p the-password-16de3b03-8504-44f9-9505-af1dc70436c4 --authenticationDatabase admin --db demo_dealership -o ./
2018-12-22T20:28:30.155+0100	writing demo_dealership.cars to 
2018-12-22T20:28:30.433+0100	done dumping demo_dealership.cars (2 documents)
```

We're going to use Mongodump with all the settings, we're going to go to demo_dealership and the output is going to be into
the working folder which is this Desktop. Because we're tunneled into the production machine we can go and grab that data from 
there and back it up locally.




