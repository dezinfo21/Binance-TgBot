from mongoengine import Document, IntField, BooleanField


class PostModel(Document):
    post_id = IntField()
    to_delete = BooleanField(default=True)

    meta = {
        "collection": "posts"
    }
