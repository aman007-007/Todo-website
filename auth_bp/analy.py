from flask import render_template,Blueprint,request,redirect,url_for,flash
analy=Blueprint('analy',__name__)
import numpy as np 
import pandas as pd 
#impport database connection
from database.db import get_db

# Define the analysis route here we will fetch the data from the database and perform the analysis and then render the analysis.html template with the analysis results
@analy.route("/analysis")
def analysis():
    conn=get_db()
    cur=conn.cursor()
    query="SELECT status from task"
    cur.execute(query)
    result=cur.fetchall()
    arr=np.array(result)
    size=arr.size
    pending,work,done=0,0,0
    for i in result:
        if i[0]=='pending':
            pending+=1
        elif i[0]=='working':
            work+=1
        else:
            done+=1
    pending_avg=pending/size*100
    work_avg=work/size*100
    done_avg=done/size*100
    df=pd.DataFrame({
        'status': ['pending', 'work', 'done'],
        'count': [pending, work, done],
        'average':[pending_avg,work_avg,done_avg]
    })
    table_html=df.to_html(classes='table',index=False)
    return render_template('analysis.html',table=table_html)