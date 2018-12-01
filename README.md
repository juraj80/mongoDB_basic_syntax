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

`db.Book.find({"Ratings.Value": 9}).count()
`

Q: How many books have been rated with 8 or above?

`db.Book.find({"Ratings.Value": {$gte: 8}}).count()
`

Q: How many books have been rated above 8?

`db.Book.find({"Ratings.Value": {$gt: 8}}).count()
`

Q: How many books have primes ratings ?

`db.Book.find({"Ratings.Value": {$in: [1,2,3,5,7] }  }).count()
`

