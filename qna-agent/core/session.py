from collections import deque
from functools import wraps
from threading import Lock

def singleton(cls):
    instances = {}
    lock = Lock()
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Session:
    def __init__(self, max_length=6):
        self.max_length = max_length
        self.histories = {}

    def flush(self, session_id):
        if session_id in self.histories:
            del self.histories[session_id]

    def add_message(self, session_id, role, content):
        if session_id not in self.histories:
            self.histories[session_id] = deque(maxlen=self.max_length)

        self.histories[session_id].append({"role": role, "content": content})

    def get_history(self, session_id, role=None):
        if session_id not in self.histories:
            return []

        if role is None:
            return list(self.histories[session_id])
        else:
            return [msg['content'] for msg in self.histories[session_id] if msg["role"] == role]
