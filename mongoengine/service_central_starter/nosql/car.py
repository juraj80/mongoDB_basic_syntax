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
    service_history = mongoengine.EmbeddedDocumentListField(ServiceHistory)

    meta = {
        'db_alias':'core',
        'collection': 'cars',
    }

