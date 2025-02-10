from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId  # Ensure ObjectId is used for MongoDB IDs
import os

app = Flask(__name__)

# Use environment variables for MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set. Check your environment variables.")

client = MongoClient(MONGO_URI) 

db = client["college"]
collection = db["students"]
collection.create_index("roll_no", unique=True)

@app.route('/')
def index():
    students = list(collection.find())  # Convert cursor to list to avoid cursor exhaustion
    return render_template("index.html", students=students) 

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_no = request.form['roll_no']
    gender = request.form['gender']
    dob = request.form['dob']
    department = request.form['department']
    year = int(request.form['year'])
    fees_paid = float(request.form["fees_paid"])
    try:
       collection.insert_one({"name": name, "roll_no": roll_no, "gender": gender,"dob": dob,"department": department,"year": year, "fees_paid": fees_paid})
       return redirect(url_for('index'))
    except DuplicateKeyError:
        return "Student with roll no already exists", 400


@app.route('/delete/<student_id>')
def delete_student(student_id):
    try:
        collection.delete_one({"_id": ObjectId(student_id)})
    except:
        pass  # Handle invalid ObjectId errors
    return redirect(url_for('index'))

@app.route('/update/<student_id>', methods=['POST'])
def update_student(student_id):
    try:
        name = request.form['name']
        roll_no = request.form['roll_no']
        gender = request.form['gender']
        dob = request.form['dob']
        department = request.form['department']
        year = int(request.form['year'])
        fees_paid = float(request.form["fees_paid"])
        collection.update_one({"_id": ObjectId(student_id)}, {"$set": {"name": name, "roll_no": roll_no, "gender": gender,"dob": dob,"department": department,"year": year, "fees_paid": fees_paid}})
    except:
        pass  # Handle invalid ObjectId errors
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
