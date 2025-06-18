from main_api.core import DB
from .config import cfg
from .database import ManageDB

db = ManageDB(cfg.DBNAME)
