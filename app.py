from flask import Flask, render_template, request, jsonify
import db

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/our-courses")
def courses():
    return render_template("courses.html")

@app.route("/contact", methods=["POST"])
def contact():
    data=request.get_json()
    fname = data.get("fname")
    lname = data.get("lname")
    email = data.get("email")
    msg = data.get("message")
    print(fname, lname, email, msg)
    return jsonify("Hello world")
if __name__=="__main__":
    app.run(debug=True)