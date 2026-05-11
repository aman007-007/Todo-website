from flask import Flask, render_template
from auth_bp.reg import auth_bp # Import the auth_bp blueprint from the reg.py file
from auth_bp.log import log # Import the log blueprint from the log.py file
from auth_bp.analy import analy  # Import the analy blueprint from the analy.py file
from auth_bp.task import task_bp # Import the task_bp blueprint from the task.py file

app = Flask(__name__)
app.secret_key = 'secret123'

app.register_blueprint(auth_bp) 
app.register_blueprint(log)
app.register_blueprint(analy)
app.register_blueprint(task_bp)

# Define the home route
@app.route('/')
def home():
    return render_template('reg.html') 

# Define the registration route  after clicking the register button and logout button
@app.route('/reg')
def reg():
    return render_template("reg.html")

if __name__ == '__main__':
    app.run(debug=True,port=8000)
    
