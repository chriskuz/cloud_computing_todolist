## Imports
from flask import Flask, render_template, redirect, g, request, url_for
import sqlite3
import requests


## Pre-instantiation
DATABASE = 'todolist.db' #-#
#-# this is a file name
#-# it reads and writes into that file
#-# it doesn't show detail....the SQL does all the manipulation

app = Flask(__name__) #always needed; makes app work. config method removed as unecessary

## Functions and Environment

#Route to root (REFACTORED)
@app.route("/")
def show_list():
      resp = requests.get("http://localhost:5001/api/items") #this may need to be changed
      resp = resp.json()
      return render_template('index.html', todolist=resp)


#Route for adding things
@app.route("/add", methods=['POST']) #only if the function is a POST request, then this function will be used to handle that request. /add is not a function...it's just a match to an "action" in HTML.
def add_entry():
    data = {
        "what_to_do": requests.form["what_to_do"],
        "due_date": requests.form["due_date"],
        "status": requests.form.get["status", "incomplete"]
    }
    requests.post("http://localhost:5001/api/add", json=data)
    return redirect(url_for('show_list')) #this comomand is important




@app.route("/add", methods=['POST']) #only if the function is a POST request, then this function will be used to handle that request. /add is not a function...it's just a match to an "action" in HTML.
def add_entry():
    db = get_db()
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
               [request.form['what_to_do'], request.form['due_date']])
    db.commit() #this is making the change in the database
    return redirect(url_for('show_list')) #this comomand is important

#Route for deleting things
@app.route("/delete/<item>")
def delete_entry(item):
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    db.commit()
    return redirect(url_for('show_list'))


#Route for marking things
@app.route("/mark/<item>")
def mark_as_done(item):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    db.commit()
    return redirect(url_for('show_list'))

#Database route
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db

#Route for error
@app.teardown_appcontext #saves memory somehow
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

## Program Instantiation
if __name__ == "__main__":
    app.run("0.0.0.0")
    # app.run("0.0.0.0", port=80)
    # app.run("0.0.0.0", port=5000)
