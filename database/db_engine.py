from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine_db = create_engine(config.DB_URL)
session_db = sessionmaker(bind=engine_db)
