from flask import Flask, g, render_template, request

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import pandas as pd
import sqlite3

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main_better.html')

@app.route('/ask/', methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        try:
            insert_message(request)
            return render_template('ask.html', name=request.form['name'], message=request.form['message'])
        except:
            return render_template('ask.html')

@app.route('/view/',methods=["GET"])
def view():

    msgs=random_messages(2)
    return render_template('hello.html',msgs=msgs)

def get_message_db():
# return the message database, and if its first time, then create a table and return it
  try:
          return g.message_db
  except:
          g.message_db = sqlite3.connect("messages_db.sqlite")
          cmd = """
          CREATE TABLE
          IF NOT EXISTS message(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name text, 
            message text) 
          """ # replace this with your SQL query
          cursor = g.message_db.cursor()
          cursor.execute(cmd)
          return g.message_db



def insert_message(request):
    # inser the message into the database by committing
    conn= get_message_db()
    name= request.form.get("name",'')
    message= request.form.get("message",'')
    cmd = f"""
    INSERT INTO message values(null,'{name}','{msg}')
    """ 
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()
    return 


def random_messages(n=2):
    # this is where we output
    out=[]
    # sql command, n can be changed according to input
    cmd=f"SELECT * FROM message ORDER BY RANDOM() LIMIT {n}"

    for i in range(n):
        conn=get_message_db()
        cursor=conn.cursor()
        cursor.execute(cmd)
        fetch=cursor.fetchone()
        out.append(fetch)

    cursor.close()
    conn.close()
    return out






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    get_message_db()