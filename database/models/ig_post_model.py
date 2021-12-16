from mongoengine import Document, StringField, DateTimeField


class IGPostModel(Document):
    symbol = StringField(required=True)
    date = DateTimeField(required=True)

    meta = {
        "collection": "ig_posts"
    }
