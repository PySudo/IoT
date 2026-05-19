from fastapi import FastAPI, Body
from .database import ManageDB
from .config import cfg
from .functions import isValid

DB = ManageDB(cfg.DBNAME)
app = FastAPI()