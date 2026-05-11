from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import get_db
log = Blueprint('log', __name__)

# Define the login route here we will check the login credentials and if they are correct then we will redirect to the user page otherwise we will flash a message and redirect to the login page
conn=get_db()
def check_login(email):
    conn = get_db()
    cur = conn.cursor()
    query="SELECT * FROM Registration WHERE email = %s"
    cur.execute(query,(email,))
    result=cur.fetchone()
    return result
    
#here submit_login function will be called when the user clicks on the login button and it will check the login credentials and if they are correct then it will redirect to the user page otherwise it will flash a message and redirect to the login page
@log.route("/submit_login", methods=["POST"])
def submit_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        result = check_login(email)
        if result:
            if result[3]==password:
              return redirect(url_for('task.user'))
            else:
                flash("wrong password")
                return redirect(url_for('log.login'))
        else:
            flash("You Din't Registration, So reg first")
            return redirect(url_for('log.login'))


# Define the login route here we will render the login.html template
@log.route('/login')
def login():
    return render_template("log.html")