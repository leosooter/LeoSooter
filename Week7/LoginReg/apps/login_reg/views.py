from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Question

def index(request):
    print "Index Route"
    # Code to display errors once on page and then erase on reload
    try:
        request.session['errors']
    except KeyError:
        request.session['errors'] = {}
        request.session['reset_errors'] = False

    print len(request.session['errors']), request.session['reset_errors']
    if len(request.session['errors']) > 0 and request.session['reset_errors']:
        print "reseting errors"
        request.session['errors'] = {}
        request.session['reset_errors'] = False
    elif len(request.session['errors']) > 0:
        request.session['reset_errors'] = True
    else:
        print "No errors"
    return render(request, 'login_reg/index.html')

def success(request):
    print "Success Route"
    users = User.objects.all()
    questions = Question.objects.all()
    context = {
        'users' : users,
        'questions' : questions,
    }
    return render(request, 'login_reg/success.html', context)

def account(request):
    print "Account Route"
    print request.session['user']['id']
    try:
        user = User.objects.get(id=request.session['user']['id'])
    except KeyError:
        print "User not logged in"
        return redirect('/')
    questions = Question.objects.filter(user=user)
    print "Q1=", questions[0].question
    context = {
        'question1' : questions.get(number=1),
        'question2' : questions.get(number=2),
        'question3' : questions.get(number=3),
        'note' : "",
    }

    return render(request, 'login_reg/account.html', context)

def update(request):
    print "Update Route"
    if request.method == 'POST':
        form = request.POST
        form_data = {
            'first_name' : form['update_first_name'],
            'last_name' : form['update_last_name'],
            'email' : form['update_email'],
            'birthday' : form['update_birthday'],
            'q_1' : form['update_q_1'],
            'q_2' : form['update_q_2'],
            'q_3' : form['update_q_3'],
        }
        response = User.objects.update(form_data, request.session['user']['id'])
        if response[0]:
            print "Update is successful!"
            return redirect('/success')
        else:
            print "Errors on update"
            request.session['errors'] = response[1]
            return redirect('/account')
    else:
        print "Invalid request method"
        return redirect('/logout')

def retrieve(request):
    print "Retrieve Route"
    if request.method == 'GET':
        print "Get request"

        return render(request, 'login_reg/retrieve.html')
    elif request.method == 'POST':
        print "Post request"

        return redirect('/reset')
    else:
        print "Invalid request type"
        return redirect('/logout')

def reset(request):
    print "Reset Route"
    if request.method == 'GET':
        print "Get request"

        return render(request, 'login_reg/reset.html')
    elif request.method == 'POST':
        print "Post request"

        return redirect('/success')
    else:
        print "Invalid request type"
        return redirect('/logout')

def register(request):
    print "Register Route"
    # print request.POST['register_birthday']
    # return redirect('/')
    if request.method == 'POST':
        form = request.POST
        form_data = {
            'first_name' : form['register_first_name'],
            'last_name' : form['register_last_name'],
            'email' : form['register_email'],
            'birthday' : form['register_birthday'],
            'password' : form['register_password'],
            'c_password' : form['register_c_password'],
        }
        response = User.objects.register(form_data)
        #response[0] is True or False- Registration was successful
        #response[1] is object containing user information on success- object containing error notes on failure
        print response[0], response[1]
        if response[0]:
            print "Registration complete"
            request.session['user'] = response[1]
            return redirect('/account')
        else:
            print "Registration form has errors"
            request.session['errors'] = response[1]
            return redirect('/')
    else:
        print "Invalid request method"
        return redirect('/logout')


def login(request):
    print "Login Route"
    if request.method == 'POST':
        form = request.POST
        form_data = {
            'email' : form['login_email'],
            'password' : form['login_password'],
        }
        response = User.objects.login(form_data)
        #response[0] is True or False- Registration was successful
        #response[1] is object containing user information on success- object containing error notes on failure
        if response[0]:
            print "Login Success"
            request.session['user'] = response[1]
            return redirect('/success')
        else:
            request.session['errors'] = response[1]
            return redirect('/')
    else:
        print "Invalid request method"
        return redirect('/logout')

def logout(request):
    print "Logout Route"
    try:
        request.session.clear()
    except KeyError:
        print "User already logged out"

    return redirect('/')
