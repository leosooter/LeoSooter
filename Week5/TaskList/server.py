from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector


app = Flask(__name__)
mysql = MySQLConnector(app, 'tasks')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def show():
    tasks = mysql.query_db("SELECT * FROM tasks")
    return render_template('/partials/tasks.html', tasks=tasks)

@app.route('/tasks/new', methods=['POST'])
def new():
    print "Adding new task"
    query = "INSERT INTO tasks (task, complete, created_at, updated_at) VALUES (:task, '', NOW(), NOW() )"
    data = { 'task' : request.form['task_desc_add'] }
    mysql.query_db(query, data)
    return redirect('/tasks')

@app.route('/tasks/update/<id>', methods=['POST'])
def update(id):
    query = "UPDATE tasks SET task = :task_text WHERE id = :id"
    data = {
    'id' : id,
    'task_text' : request.form['task_desc_edit'],
    }
    mysql.query_db(query, data)
    return redirect('/tasks')

@app.route('/tasks/complete/<id>/<comp>', methods=['post'])
def complete(id, comp):
    if comp == "True":
        complete = "checked"
    else:
        complete = ""
    query = "UPDATE tasks SET complete = :complete WHERE id = :id"
    data = {
        'id' : id,
        'complete' : complete
        }
    mysql.query_db(query, data)
    return redirect('/tasks')

@app.route('/tasks/delete/<id>', methods=['POST'])
def delete(id):
    query = "DELETE FROM tasks WHERE id = :id"
    data = { 'id' : id}
    mysql.query_db(query, data)
    return redirect('/tasks')

app.run(debug=True)
