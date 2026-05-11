import psycopg2
from flask import render_template
# Database connection utility
def get_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="postgres",
        user="postgres",
        password=""
    )


    

