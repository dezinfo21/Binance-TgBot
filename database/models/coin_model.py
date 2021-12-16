from __future__ import annotations

from typing import Optional
from mongoengine import Document, StringField, IntField, FloatField, ReferenceField, ListField, NULLIFY

from binance_config import DELETE_ZEROS
from .post_model import PostModel


class CoinModel(Document):
    status = StringField(required=True, default="untreated", choices=["untreated", "treated"])
    symbol = StringField(required=True, unique=True)

    last_price = FloatField()
    last_timestamp = IntField()

    price = IntField(null=True)
    timestamp = IntField(null=True)
    post = ReferenceField(PostModel, reverse_delete_rule=NULLIFY)
    entered_targets = ListField(default=[])
    open_target = IntField()

    meta = {
        "collection": "coins"
    }
