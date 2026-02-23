from flask import Flask, render_template, request, jsonify, redirect, url_for
import db
import uuid
import razorpay
import os
from dotenv import load_dotenv

load_dotenv(override=True)

key_id=os.getenv("RAZORPAY_KEY")
key_secret=os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(key_id, key_secret))
app = Flask(__name__)
@app.route("/")
def index():
    session_id=request.cookies.get("session_id")
    if session_id:
        return render_template("index.html", session_id=session_id)    
    return render_template("index.html", session_id=None)

@app.route("/logout", methods=["POST"])
def logout():
    try:
        session_id=request.cookies.get("session_id")
        if session_id:
            db.delete_session(session_id)
            response=redirect(url_for("index"))
            
        response.delete_cookie("session_id")
        return response
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500
@app.route("/registeration")
def register():
    session_id=request.cookies.get("session_id")
    if session_id:
        return render_template("index.html", session_id=session_id)
    return render_template("registeration.html")
@app.route('/validate-registration', methods=['POST'])
def valReg():
    pass

@app.route("/login")
def login():
    session_id=request.cookies.get("session_id")
    if session_id:
        return render_template("index.html", session_id=session_id)
    return render_template("login.html", session_id=None)

@app.route("/user-authentication", methods=['POST'])
def authenticate():
    try:
        data=request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}),400
        email=data['email']
        password=data['password']
        if not email or not password:
            return jsonify({"message": "All fields are required"}),400
        session_id=db.authenticate_user(email,password)
        if session_id!=-1:
            response = jsonify({'sucess':'login is sucessful'})
            response.status_code = 200
            response.set_cookie(
                "session_id",
                session_id,
                httponly=True,
                secure=False,
                samesite="Lax"
            )
            return response
        else:
            return jsonify({'error':'Mail or passord is invalid'}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/our-courses")
def courses():
    session_id=request.cookies.get("session_id")
    courses=db.fetchCourses()
    return render_template("courses.html", courses=courses, session_id=session_id)

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data=request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}),400

        fname = data.get("fname")
        lname = data.get("lname")
        email = data.get("email")
        msg = data.get("message")
        if not fname or not lname or not email or not msg:
            return jsonify({"message": "All fields are required"}),400
        db.insert_user_query(fname,lname,email,msg)
        return jsonify({"message": "Message sent successfully."}),201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/course-details/<int:course_id>")
def course_details(course_id):
    try:
        session_id=request.cookies.get("session_id")
        if session_id:

            course_data=db.fetchCourses(course_id)
            return render_template("course-details.html", session_id=session_id, course_data=course_data[0])
        else:
            return render_template('login.html')
        
    except Exception as e:
        print("Error: ", e)
def isExist(uid, cid):
    exist=db.cart(uid, cid)
    if len(exist)!=0:
        return True
    return False
@app.route("/course_op", methods=['POST']) 
def course_op():
    try:
        session_id=request.cookies.get("session_id")
        if session_id:
            data=request.form.to_dict()
            res=db.fetch_user(session_id)
            data['uid']=res['user_id']
            print (isExist(data['uid'], data['cid']))
            if isExist(data['uid'], data['cid']):
                return "already in cart"
            else:
                db.cart(data['uid'], data['cid'],1)
                return redirect(url_for('cart'))
        else:
            return render_template('login.html')
    except Exception as e:
        print("Error: ", e)

@app.route("/cart")
def cart():
    try:
        session_id=request.cookies.get("session_id")
        if session_id:
            user=db.fetch_user(session_id)
            data=db.cart(user['user_id'])
            total_price=0
            count=0
            for i in data:
                total_price=total_price+i['price']
                count+=1
            return render_template('cart.html', data=data, total_price=total_price,count=count)
        else:
            render_template('login.html')
    except Exception as e:
        print("Error: ",e)

@app.route("/create-order", methods=["POST"])
def create_order():
    session_id=request.cookies.get('session_id')
    data = request.get_json()
    
    amount=int(float(data.get('price'))*100)

    # amount = float(data["price"]) * 100  

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })
    
    res=db.fetch_user(session_id)
    db.order(res['user_id'],order['id'],amount)

    return jsonify({
        "order_id": order["id"],
        "amount": amount,
        "key_id":key_id
    })

@app.route("/verify-payment", methods=["POST"])
def verify_payment():
    print('verify')
    data = request.get_json()

    # Required fields from Razorpay response
    razorpay_payment_id = data.get("razorpay_payment_id")
    razorpay_order_id = data.get("razorpay_order_id")
    razorpay_signature = data.get("razorpay_signature")

    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        
        client.utility.verify_payment_signature(params_dict)
        
        print("This is for verify [payment]")
        db.order(order_id=razorpay_order_id, payment_id=razorpay_payment_id)

        return jsonify({"status": "success"}), 201

    except razorpay.errors.SignatureVerificationError:
        db.order_update_status(order_id=razorpay_order_id, status="failed")
        return jsonify({"status": "failed"}), 400
if __name__=="__main__":
    app.run(debug=True)