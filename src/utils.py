import uuid
from datetime import datetime

def get_uuid4():
    """
    generate uuid4 and returns in string format
    """
    id = str(uuid.uuid4())
    return id

def logger(*args):
    """
    Used as print statement, but also prints timestamp along with the args
    """
    current_time = datetime.now()
    readable_format = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    print("[" + readable_format + "]", *args)