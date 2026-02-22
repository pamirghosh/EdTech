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
DB_SSL_CA=os.getenv("DB_SSL_CA")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    connect_args={
        "ssl": {
            "ca": DB_SSL_CA
        },
        "connect_timeout": 5
    },
    pool_size=2,          
    max_overflow=1,       
    pool_timeout=10,
    pool_recycle=280,
    pool_pre_ping=True,
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

def fetchCourses(courseid=None):
    with engine.connect() as conn:
        if courseid:
            res = conn.execute(text("SELECT * FROM courses WHERE id=:courseid"),{"courseid":courseid})
        else:    
            res = conn.execute(text("SELECT * FROM courses"),{})
        rows = res.mappings().all()
        return rows

# fetch and add course to cart table
def cart(userid, courseid=None, insert=None):
    with engine.connect() as conn:
        if courseid!=None:
            if insert==None:
                res = conn.execute(text("SELECT * FROM user_cart WHERE uid=:userid AND cid=:courseid"),{"userid":userid, "courseid":courseid})
                row = res.mappings().all()
                return row
            else:
                query = text(f"INSERT INTO user_cart (cid,uid,qty) VALUES (:courseid, :userid, :qty)")
                conn.execute(query, {"courseid": courseid, "userid":userid, "qty": 0})
                conn.commit()
        else:
            print('aaa')
            res = conn.execute(text("SELECT courses.id, courses.title , courses.details, courses.image, courses.price FROM courses,user_cart WHERE courses.id=user_cart.cid and user_cart.uid=:userid"),{"userid":userid})
            row = res.mappings().all()
            return row

#fetch user id
def fetch_user(session_id):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM sessions WHERE session_id=:session_id"),{"session_id":session_id})
        row = res.mappings().first()
        return row

#insert into order table
def order(user_id=None, order_id=None, amount=None, payment_id=None):
    with engine.connect() as conn:
        if user_id!=None:
            query = text("""
                INSERT INTO orders (uid, razorpay_order_id, amount, status)
                VALUES (:uid, :order_id, :amount, :status)
            """)
            conn.execute(query, {
                "uid": user_id,
                "order_id": order_id,
                "amount": amount,
                "status": "pending"
            })
            conn.commit() 
        else:
            query = text("UPDATE orders SET razorpay_payment_id=:payment_id, status=:status WHERE razorpay_order_id = :razorpay_order_id")
            conn.execute(query, {
                "razorpay_order_id":order_id,
                "payment_id":payment_id,
                "status": 'success'
            })
            conn.commit()