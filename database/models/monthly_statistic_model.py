from mongoengine import Document, ListField, IntField


class MonthlyStatisticModel(Document):
    year = IntField(required=True)
    month = IntField(required=True)

    posts_id = ListField(required=True)

    meta = {
        "collection": "monthly_statistic"
    }
