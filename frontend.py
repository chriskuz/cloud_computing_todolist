## Imports
from flask import Flask, render_template, redirect, g, request, url_for, jsonify
import sqlite3
import requests


## Pre-instantiation
app = Flask(__name__) #always needed; makes app work. config method removed as unecessary

## Functions and Environment
back_end_port = 5002


# Root (REFACTORED)
@app.route("/")
def show_list():
      resp = requests.get(f"http://localhost:{back_end_port}/api/items") #this may need to be changed
      resp = resp.json()
      return render_template('index.html', todolist=resp)


# Add (REFACTORED)
@app.route("/add", methods=['POST']) #only if the function is a POST request, then this function will be used to handle that request. /add is not a function...it's just a match to an "action" in HTML.
def add_entry():
    data = {
        "what_to_do": request.form["what_to_do"], #note use of `request`...different from `requests`....this specific flask method is being passed in as it's meant to primarily interact with a DB
        "due_date": request.form["due_date"],
        "status": request.form.get("status", "incomplete")
    }
    requests.post(f"http://localhost:{back_end_port}/api/add", json=data)
    return redirect(url_for('show_list')) #this comomand is important


# Delete (REFACTORED)
@app.route("/delete/<item>")
def delete_entry(item):
    data = {"what_to_do": item}
    requests.post(f"http://localhost:{back_end_port}/api/delete", json=data)
    return redirect(url_for('show_list'))


# Mark (REFACTORED)
@app.route("/mark/<item>")
def mark_as_done(item):
    data = {"what_to_do": item}
    requests.post(f"http://localhost:{back_end_port}/api/mark_as_done", json=data)
    return redirect(url_for('show_list'))


## Program Instantiation
if __name__ == "__main__":
    app.run("0.0.0.0", port=5003, debug=True)
    # app.run("0.0.0.0", port=80)
    # app.run("0.0.0.0", port=5000)
