# app/monitoring.py
# small instrumentation hooks - extendable
from time import time

class Timer:
    def __enter__(self):
        self.t0 = time()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time() - self.t0

