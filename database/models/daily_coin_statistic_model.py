from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime


class DailyCoinStatisticModel(Document):
    symbol = StringField(required=True)
    percent = FloatField(required=True)
    period = StringField(required=True)

    date = DateTimeField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    meta = {
        "collection": "daily_statistic"
    }