import json
from json import JSONEncoder
import attr


class CustomEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def to_json_from(clazz):  # without attr
    validate(clazz)
    return json.dumps(clazz, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def to_dict_from_attr(clazz):
    validate(clazz)
    return attr.asdict(clazz)


def validate(clazz):
    if clazz is None:
        raise ValueError("class is null!!!")
