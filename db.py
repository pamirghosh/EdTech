from sqlalchemy import create_engine,text
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import uuid

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
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM user where email=:email and password=:password"),{'email':email, 'password':password})
        rows = res.mappings().all()
        
        if len(rows)>0:
            session_id = str(uuid.uuid4())
            print("session id: ", session_id)
            created_at = datetime.now(timezone.utc)
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            query = text(f"INSERT INTO sessions (session_id,user_id,created_at,expires_at) VALUES (:session_id, :user_id, :created_at ,:expires_at)")
            conn.execute(query, {"session_id": session_id, "user_id":rows[0]['id'], "created_at":created_at, "expires_at":expires_at})
            conn.commit()
            return session_id
        return -1

def delete_session(session_id):
    with engine.connect() as conn:
        query=text(f"Delete from sessions where session_id=:session_id")
        conn.execute(query, {"session_id":session_id})
        conn.commit()

def fectCourses():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM courses"),{})
        rows = res.mappings().all()
        return rows