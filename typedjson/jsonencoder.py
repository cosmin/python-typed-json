import typing
from datetime import datetime
from decimal import Decimal
from enum import Enum
from json import JSONEncoder

from .basemodel import BaseModel, camel


class ModelJsonEncoder(JSONEncoder):
    def default(self, o):
        if o is None:
            return o
        elif isinstance(o, str):
            return o
        elif isinstance(o, int):
            return o
        elif isinstance(o, float):
            return o
        elif isinstance(o, bool):
            return o
        elif isinstance(o, list) or isinstance(o, tuple):
            return [self.default(i) for i in o]
        elif isinstance(o, dict):
            return {k: self.default(v) for k, v in o.items()}
        elif isinstance(o, BaseModel):
            out = {}
            for key, klass in typing.get_type_hints(o.__class__).items():
                out[camel(key)] = self.default(getattr(o, key))
            return out
        elif isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.value
        else:
            return super().default(o)
