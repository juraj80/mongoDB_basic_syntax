import mongoengine
import datetime

class ServiceHistory(mongoengine.EmbeddedDocument):
    date = mongoengine.DateTimeField(default=datetime.datetime.now) # we pass here a function, we don't want to call it, could use also lambda
    description = mongoengine.StringField()
    price = mongoengine.FloatField()
    customer_rating = mongoengine.IntField(min_value=1,max_value=5)
