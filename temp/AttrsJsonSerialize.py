# https://www.attrs.org/en/stable/examples.html
# https://www.geeksforgeeks.org/attr-asdict-function-in-python/

import attr


@attr.s
class Coordinates(object):
    # attributes
    x = attr.ib()
    y = attr.ib()


c1 = Coordinates(1, 2)
print(c1)
print(attr.asdict(c1))
