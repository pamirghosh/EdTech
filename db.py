from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os

load_dotenv(override=True)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SSL_CA="D:/edtech/ca.pem"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    connect_args={
        "ssl": {
            "ca": DB_SSL_CA
        }
    },
    pool_pre_ping=True,
    pool_recycle=280,
    echo=False
)

# with engine.connect() as conn:
#   res = conn.execute(text("SELECT * FROM user_queries"))
#   rows = res.mappings().all()
#   print(rows)