from flask import Flask, render_template, request, jsonify
import db

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

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
        if len(db.authenticate_user(email,password))==1:
            return jsonify({'sucess':'login is sucessful'}), 201
        else:
            return jsonify({'error':'Mail or passord is invalid'}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/our-courses")
def courses():
    return render_template("courses.html")

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

if __name__=="__main__":
    app.run(debug=True)