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

def insert_user_query(fname, lname, email, msg):
  with engine.connect() as conn:
        query = text(f"INSERT INTO user_queries (fname, lname, email, message) VALUES (:fname, :lname, :email, :msg)")
        conn.execute(query, {"fname": fname, "lname":lname, "email": email, "msg": msg})
        conn.commit()
def authenticate_user(email, password):
    print("Hello eo")
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM user where email=:email and password=:password"),{'email':email, 'password':password})
        rows = res.mappings().all()
        print(rows)
        return rows