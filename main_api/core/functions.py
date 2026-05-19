from hashlib import md5
from .config import cfg

def isValid(key):
    return cfg.KEY == md5(key.encode()).hexdigest()