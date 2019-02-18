import typing
from enum import Enum


def camel(snake_str):
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


class BaseModel:
    def __init__(self, **kwargs):
        allowed = typing.get_type_hints(self.__class__).keys()
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)
            else:
                raise KeyError("Key is not alowed: %s" % k)

    @classmethod
    def parse(cls, dct: dict):
        if not dct:
            return None

        # using __dict__ rather than hasattr because we only want it
        # to match on the top level class not any subclasses
        if '_subclass_map' in cls.__dict__:
            the_type = dct.get('type')
            if the_type in cls._subclass_map:
                value = cls._subclass_map[the_type].parse(dct)
                value.type = the_type
                return value
        elif '_subclasses' in cls.__dict__:
            for kwargs, klass in cls._subclasses:
                match = True
                for k, v in kwargs.items():
                    if dct.get(k) != v:
                        match = False
                        break
                if match:
                    value = klass.parse(dct)
                    for k, v in kwargs.items():
                        setattr(value, k, v)
                    return value

        instance = cls()

        for key, klass in typing.get_type_hints(cls).items():
            is_list = False
            if klass == list:
                klass = getattr(instance, key)
                setattr(instance, key, [])
                is_list = True

            if key in dct:
                value = dct[key]
            elif camel(key) in dct:
                value = dct[camel(key)]
            else:
                continue

            if is_list:
                lst = []
                if value is not None:
                    for item in value:
                        if klass is not None and issubclass(klass, BaseModel):
                            lst.append(klass.parse(item))
                        else:
                            lst.append(item)
                setattr(instance, key, lst)  # set to empty list if key is omitted or None to make looping easier
            elif value is None:
                setattr(instance, key, None)  # preempt trying to parse this below
            else:
                if issubclass(klass, BaseModel):
                    setattr(instance, key, klass.parse(value))
                elif issubclass(klass, Enum):
                    setattr(instance, key, klass(value))
                else:
                    setattr(instance, key, value)
        return instance


def typedmodel(klass):
    subclass_map = {}
    klass.type: str = None

    def subclass_hook(cls, type=None):
        super(cls).__init_subclass__()
        if type is not None:
            subclass_map[type] = cls

    klass._subclass_map = subclass_map
    klass.__init_subclass__ = classmethod(subclass_hook)
    return klass


def attributemodel(klass):
    subclasses = []

    def subclass_hook(cls, **kwargs):
        super(cls).__init_subclass__()
        if kwargs:
            subclasses.append((kwargs, cls))
            subclasses.sort(key=lambda x: len(x[0].keys()), reverse=True)

    klass._subclasses = subclasses
    klass.__init_subclass__ = classmethod(subclass_hook)
    return klass
