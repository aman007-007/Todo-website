from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import get_db
auth_bp = Blueprint('auth', __name__)

# Define the registration route here we will check the registration credentials and if they are correct then we will redirect to the login page otherwise we will flash a message and redirect to the registration page
conn=get_db()
def check_registration(username, email, password):
    conn = get_db()
    cur = conn.cursor()
    query="""SELECT * FROM Registration
    WHERE name =%s
    AND email =%s
    AND password =%s"""
    cur.execute(query,(username, email, password))
    result=cur.fetchone()
    if result==None:
        query="""
        INSERT INTO Registration(name, email, password)
        VALUES(%s,%s,%s)
        """
        cur.execute(query,(username, email, password))
        conn.commit()
        return None
    else:
      return result
    
#here submit_registration function will be called when the user clicks on the register button and it will check the registration credentials and if they are correct then it will redirect to the login page otherwise it will flash a message and redirect to the registration page
@auth_bp.route("/submit_registration", methods=["POST"])
def submit_registration():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        result = check_registration(username, email, password)
        if result:
            flash("You have already registered. Please log in.")
            return render_template("reg.html")
        else:
            flash("Registration successful! Please log in.")
            return render_template("log.html")