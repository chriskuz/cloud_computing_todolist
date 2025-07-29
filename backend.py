## Imports
from flask import Flask, render_template, redirect, g, request, url_for, jsonify
import sqlite3
import requests


## Pre-instantiation
DATABASE = 'todolist.db' 

## App Execution and Config
app = Flask(__name__)
app.config.from_object(__name__)

## Functions and Environment

# Root (REFACTORED)
@app.route("/api/items") 
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries]
    return jsonify(tdlist)


# Add (REFACTORED)
@app.route("/api/add", methods=["POST"])
def add_entry():
    data = request.get_json()  # this pulls JSON payload from frontend's requests.post
    what_to_do = data.get("what_to_do")
    due_date = data.get("due_date")
    status = data.get("status", "incomplete")  # fallback default

    db = get_db()
    db.execute("INSERT INTO entries (what_to_do, due_date, status) VALUES (?, ?, ?)", (what_to_do, due_date, status))
    db.commit()
    return jsonify({"success": True})


# Delete (REFACTORED)
@app.route("/api/delete", methods=["POST"])
def delete_entry():
    data = request.get_json()
    what_to_do = data.get("what_to_do")

    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do=?", (what_to_do,))
    db.commit()
    return jsonify({"success": True})


# Mark (REFACTORED)
@app.route("/api/mark_as_done", methods=["POST"])
def mark_as_done():
    data = request.get_json()
    what_to_do = data.get("what_to_do")

    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do=?", (what_to_do,))
    db.commit()
    return jsonify({"success": True})

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
    app.run("0.0.0.0", port=5002, debug=True)
    # app.run("0.0.0.0", port=80)
    # app.run("0.0.0.0", port=5000)
