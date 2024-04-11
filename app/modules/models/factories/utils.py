from datetime import datetime


def time_hash():
    return hex(hash(datetime.utcnow()))[-10:]
