from datetime import datetime
from mongoengine import ( Document, StringField, DateTimeField, ListField)
import random
class Order(Document):
    create_time = DateTimeField(default=datetime.now())
    content = StringField(required=True)
    address = StringField(required=True)
    status = StringField(default="收到訂單")
    lat = ListField(default=[random.randint(0,200),random.randint(0,200)])
