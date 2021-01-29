from flask import Flask, render_template, request, jsonify
import sqlite3
import os
app = Flask(__name__)

def get_db():
    db=sqlite3.connect('db.sqlite3')
    db.row_factory = sqlite3.Row
    return db

def create_db():
    db = get_db()
    db.execute('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT)')
    db.close()

if not os.path.isfile('db.sqlite3'):
    create_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/user', methods=['POST', 'PUT'])
def user():
    json_data = request.get_json(force=True)

    # POST Method implementation
    if request.method == 'POST':
        
        # Check if the JSON contain "user"
        if 'user' not in json_data:
            return {"Error": "Payload should be in JSON {user:<string>}."}
        else:
            myUser = json_data['user']  

        response = ""
        db = get_db()
        user = db.execute('SELECT user FROM user WHERE user = ?', (myUser,)).fetchall()

        if len(user):
            response =  {"Error":  myUser + ' is already in our records. Please try with another user.'}
        else:
            db.execute('INSERT INTO user(user) VALUES (?)', (myUser,))
            response = {"Success": myUser + " is registered! Have a wonderful day!"}
        
        db.commit()
        db.close()
        return response
    
    # PUT Method implementation
    if request.method == 'PUT':

        # Check if the JSON contain "newuser" and "olduser"
        if 'olduser' and 'newuser' not in json_data:
            return {"Error" : 'Payload should be in JSON {olduser:<string>, newuser:<string>}.'}
        else:
            newUser = json_data['newuser']
            oldUser = json_data['olduser']

        response = ""
        db = get_db()
        oldUserExist = db.execute('SELECT user FROM user WHERE user = ?', (oldUser,)).fetchall()
        newUserExist = db.execute('SELECT user FROM user WHERE user = ?', (newUser,)).fetchall()
        if len(oldUserExist) == 0:
            response = {"Error" : 'User '  + oldUser + ' is not in our record. Please try again.'}
        elif len(newUserExist) != 0:
            response = {"Error" : 'User you are replacing is already in our record.'}
        else: 
            db.execute('UPDATE user SET user = ? WHERE user = ?', (newUser, oldUser))
            db.commit()
            response = {"Success": newUser + " has been updated to replace " + oldUser + "."}

        db.close()
        return response 


# GET Method implementation
@app.route('/getUser')
def getUser():

    myUser = request.args['user']
    response = ""

    if myUser != "":
        db  = get_db()
        user = db.execute('SELECT user FROM user WHERE user = ?', (myUser,)).fetchall()
        if len(user) == 0:
            response = 'Error: ' + myUser + ' is not in our record. Please try again.'
        else:
            response = "Welcome, " + user[0]['user'] + "!"

        db.commit()
        db.close()
    
    return response


if __name__ == "__main__":
    app.run(debug=True)