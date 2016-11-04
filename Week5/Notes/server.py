from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector


app = Flask(__name__)

mysql = MySQLConnector(app, 'notes')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes')
def show():
    notes = mysql.query_db("SELECT * FROM notes")
    return render_template('/partials/notes.html', notes = notes)

@app.route('/notes/new', methods=['POST'])
def create():
    title = request.form['title']
    description = request.form['description']

    query = "INSERT INTO notes (title, description, created_at, updated_at) VALUES (:title, :description, NOW(), NOW() )"
    data = {
        'title' : title,
        'description' : description,
    }
    mysql.query_db(query, data)
    return redirect('/notes')

@app.route('/notes/update/<id>', methods=['POST'])
def update(id):
    description = request.form['description']
    query = "UPDATE notes SET description = :description WHERE id = :id"
    data = {
        'description' : description,
        'id' : id,
    }
    mysql.query_db( query, data)
    return redirect('/notes')

@app.route('/notes/destroy/<id>', methods=['POST'])
def destroy(id):
    query = "DELETE FROM notes WHERE id = :id"
    data = { 'id' : id }
    print "deleting note: " , data
    mysql.query_db(query, data)
    return redirect('/notes')

app.run(debug=True)
