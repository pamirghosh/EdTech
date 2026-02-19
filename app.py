from flask import Flask, render_template, request, jsonify, redirect, url_for
import db
import uuid

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
                secure=True,
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
    

if __name__=="__main__":
    app.run(debug=True)