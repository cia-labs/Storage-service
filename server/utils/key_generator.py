import threading
import os
import sys
from app.crud.crud import get_latest_generated_key

class KeyGenerator:
    def __init__(self):
        self.lock = threading.Lock()
        self.initial_value = None
        self.counter = 0

    def _initialize_counter(self):
        if self.initial_value is None:
            self.initial_value = get_latest_generated_key()
            self.counter = int(self.initial_value)

    def generate_key(self):
        self._initialize_counter()
        with self.lock:
            key = self.counter + 1
            self.counter = key
            return str(key)

    