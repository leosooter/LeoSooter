from flask import Flask, render_template, request, redirect, flash, session, jsonify
from mysqlconnection import MySQLConnector
import math


app = Flask(__name__)
app.secret_key = 'supersecret'

mysql = MySQLConnector(app, 'lead_gen_business')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<first_name>/<last_name>/<date_from>/<date_to>/<order_by>/<srt>/<page>/<per_page>')
def search(first_name,last_name,date_from,date_to,order_by,srt,page,per_page):
    print "running search route"
    #This is a security feature to pass field-names into the ORDER BY of the SQL query. The user's input is never added
    #it is compared against a list of safe values and one of those values is passed in if it is a match.
    #Vishnu helped me think through the setup of this.
    o_by = 'leads_id'
    field_list = ['leads_id', 'first_name', 'last_name', 'registered_datetime', 'email']
    for index in range(len(field_list)):
        if field_list[index] == order_by:
            o_by = field_list[index]

    #another quick security check of the same type to allow dynamic sorting
    #the function will default to ASC so passing ASC in the url is redundant, but
    #I think it improves readablility and makes it easier to debug
    sort = 'ASC'
    if srt == 'DESC':
        sort = 'DESC'

    #find the start point to return results from. If the page is one the start is one
    #otherwise the start point will be the page number times the number of results per page(per_page)
    if page == '1':
        start = 0
    else:
        start = (int(page) * int(per_page))
    #query the database to find the total number of results matching the user's search
    count_query = "SELECT COUNT(leads_id) AS count FROM leads WHERE first_name LIKE :first_name AND last_name LIKE :last_name AND registered_datetime BETWEEN :date_from AND :date_to"
    #Query the database for the results for the current page
    query = "SELECT * FROM leads WHERE first_name LIKE :first_name AND last_name LIKE :last_name AND registered_datetime BETWEEN :date_from AND :date_to ORDER BY {} {} LIMIT :start, :per_page".format(o_by,sort)
    data = {
        'first_name' : first_name,
        'last_name' : last_name,
        'date_from' : date_from,
        'date_to' : date_to,
        'start' : start,
        'per_page' : int(per_page),
    }
    results = mysql.query_db(query, data)
    for key in data:
        print key, data[key]
    page_count = int(math.ceil(int(mysql.query_db(count_query, data)[0]['count'])/ int(per_page)))
    print "page count = ", page_count
    if page_count <= 1:
        page_count = 1

    print "Results = ", results
    return render_template('/partials/results.html', page_count=page_count, results=results)

app.run(debug=True)
