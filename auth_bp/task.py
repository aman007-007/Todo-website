from flask import Blueprint, render_template, redirect, url_for, flash, request
from database.db import get_db

task_bp = Blueprint('task', __name__)

# Function to add a task to the database
def add_task_db(title,description,priority,status):
    conn=get_db()
    cur=conn.cursor()
    query="""INSERT INTO task(title,description,priority,status)
    VALUES(%s,%s,%s,%s)"""
    cur.execute(query,(title,description,priority,status))
    conn.commit()

    
    cur.close()
    conn.close()
    return 1

# Define the route to add a task here we will get the task details from the form and then call the add_task_db function to add the task to the database and then redirect to the user page
@task_bp.route("/add_task", methods=["POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description").upper()
        priority=request.form.get("priority")
        result=add_task_db(title,description,priority,'pending')
        if result==1:
            return redirect(url_for('task.user'))
        else:
            return "fail"

        

# Define the route to display the tasks here we will fetch the tasks from the database and then render the task.html template with the tasks data
@task_bp.route("/task")
def task():
    conn=get_db()
    cur=conn.cursor()
    query="""SELECT * FROM task"""
    cur.execute(query)
    result=cur.fetchall()
    conn.commit()

    
    cur.close()
    conn.close()
    return render_template('task.html', data=result)


# Define the route to clear the tasks here we will truncate the task table and then redirect to the user page
@task_bp.route("/clear")
def clear():
    conn=get_db()
    cur=conn.cursor()
    query="TRUNCATE TABLE task RESTART IDENTITY"
    cur.execute(query)
    conn.commit()
    conn.close()
    return redirect(url_for('task.user'))


# Define the route to change the task status here we will get the task id from the url and then fetch the task details from the database and then change the status of the task and then redirect to the user page
@task_bp.route("/change/<int:id>",methods=["POST"])
def change(id):
    if request.method=="POST":
        conn=get_db()
        cur=conn.cursor()
        query="SELECT * FROM task WHERE id =%s"
        cur.execute(query,(id,))
        result=cur.fetchone()
        if result[4]=="pending":
            query="UPDATE task SET status=%s WHERE id=%s"
            cur.execute(query,("working",id))
        elif result[4]=="working":
            query="UPDATE task SET status=%s WHERE id=%s"
            cur.execute(query,("done",id))
        else:
            query="UPDATE task SET status=%s WHERE id=%s"
            cur.execute(query,("pending",id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('task.user'))
    
# Define the route to delete a task here we will get the task id from the url and then delete the task from the database and then redirect to the user page
@task_bp.route("/delete/<int:id>",methods=["POST"])
def delete(id):
    if request.method=="POST":
        conn=get_db()
        cur=conn.cursor()
        query="DELETE  FROM task WHERE id =%s"
        cur.execute(query,(id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('task.user'))

# Define the route to display the user page here we will fetch the tasks from the database and then render the task.html template with the tasks data
@task_bp.route("/user")
def user():
    conn=get_db()
    cur=conn.cursor()
    query="SELECT * FROM task ORDER BY id ASC"
    cur.execute(query)
    data=cur.fetchall()
    return render_template("task.html",data=data)