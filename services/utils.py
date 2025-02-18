from datetime import datetime as dt
from uuid import uuid4


def ts():
    a = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    return a


def uuidg(prefix=None):
    uuid_short = str(uuid4())[-8:]
    if prefix is not None:
        uuid_short = prefix + uuid_short
    # uuid_long = str(uuid4())
    return uuid_short.upper()
