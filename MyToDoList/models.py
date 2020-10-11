from datetime import datetime
from mongoengine import ( Document, StringField, DateTimeField)
class Order(Document):
    create_time = DateTimeField(default=datetime.now())
    content = StringField(required=True)
    address = StringField(required=True)
    status = StringField(default="收到訂單")