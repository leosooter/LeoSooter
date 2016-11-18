from __future__ import unicode_literals
from django.db import models
import re, time
import bcrypt

class UserManager(models.Manager):
    #Process registrations- adds user to DB if valid- returns a tuple
    #first value in tuple is true or false- registration is valid
    #second value returns an error notes object if form has errors, or a user info object if form is valid
    def register(self, form_data):
        print "Register Method"
        error_notes = {}
        #check to make sure no fields are blank
        for key, value in form_data.items():
            print "arg length=", len(value)
            if len(value) == 0:
                print "Field without value found"
                error_notes[key] = "This field cannot be blank"
                return (False, error_notes)

        #Validate first_name
        if User.objects.validateName(form_data['first_name']):
            print "first_name is valid"
        else:
            print "first_name not valid"
            error_notes['first_name'] = "First name must be at least 2 letters and no numbers"
            return (False, error_notes)

        #Validate last_name
        if User.objects.validateName(form_data['last_name']):
            print "last_name is valid"
        else:
            print "last_name not valid"
            error_notes['last_name'] = "last name must be at least 2 letters and no numbers"
            return (False, error_notes)

        if User.objects.validateBirthday(form_data['birthday']):
            print "birthday is valid"
        else:
            print "birthday is not valid"
            error_notes['birthday'] = "Please enter a valid birthday"
            return (False, error_notes)

        # validate email returns tuple (valid, user-object if in DB- False if not) Check to make sure return is (True, False)-
        # email is valid, and not in DB
        email_valid = User.objects.validateEmail(form_data['email'])
        if email_valid[0]:
            print "Email format is valid"
            if not email_valid[1]:
                print "Email in not duplicate"
            else:
                print "Email is already in DB"
                error_notes['email'] = "The email you entered is already registered to an account. Please use a different email or login below"
                return (False, error_notes)
        else:
            print "Email format not valid"
            error_notes['email'] = "Please enter a valid email"
            return (False, error_notes)
        #Validate Password
        password_valid = User.objects.validatePassword(form_data['password'], form_data['c_password'])
        if password_valid[0]:
            print "Password is valid format"
            if password_valid[1]:
                print "Password matches confirm_password"
            else:
                print "Password does not match confirm_password"
                error_notes['c_password'] = "Password and confirmation password do not match"
                return (False, error_notes)
        else:
            error_notes['password'] = "Password must be at least 8 characters long with at least one capital and number"
            return (False, error_notes)

        print "Registration is Valid!"
        password = bcrypt.hashpw(form_data['password'].encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
        new_user = User.objects.create(first_name=form_data['first_name'], last_name=form_data['last_name'], email=form_data['email'], birthday=form_data['birthday'], password=password)
        new_user.save()
        # Create blank security questions for new user- they will be sent to the account page to set the answers for these.
        print "//New User Id=",new_user.id
        new_question = Question.objects.create(number=1, question='What city were you born in?', answer="", user=new_user)
        new_question.save()
        new_question = Question.objects.create(number=2, question='What was the name of your first pet?', answer="", user=new_user)
        new_question.save()
        new_question = Question.objects.create(number=3, question='What is your favorite coding language?', answer="", user=new_user)
        new_question.save()
        user = User.objects.loginUser(new_user)
        return (True, user)


    def login(self, form_data):
        #Process logins- returns a tuple
        #first value in tuple is true or false- login is valid
        #second value returns an error notes object if form has errors, or a user info object if form is valid
        print "Login Method"
        error_notes = {}
        #check to make sure no fields are blank
        for key, value in form_data.items():
            print "arg length=", len(value)
            if len(value) == 0:
                print "Field without value found"
                error_notes[key] = "This field cannot be black"
                return (False, error_notes)
        # validate email returns tuple (valid, user-object if in DB- False if not) Check to make sure return is (True, True)-
        # email is valid, and already in DB
        email_valid = User.objects.validateEmail(form_data['email'])
        if email_valid[0]:
            print "Email format is valid"
            if not email_valid[1]:
                print "Email not found in DB"
                error_notes['login_email'] = "No account matches the email you entered. Please use a different email or register a new account"
                return (False, error_notes)
            else:
                print "Email found in DB"
                user = email_valid[1][0]
                password_valid = User.objects.validatePassword(form_data['password'], 'none')
                if password_valid[0]:
                    print "Password is valid format"
                    password = form_data['password'].encode(encoding="utf-8", errors="strict")
                    hashed_password = user.password.encode(encoding="utf-8", errors="strict")
                    if bcrypt.hashpw(password, hashed_password) == hashed_password:
                        print "Login Successful!"
                        user = User.objects.loginUser(user)
                        return (True, user)
                    else:
                        print "Password does not match record"
                        error_notes['login_password'] = "The password you entered doe not match our records"
                        return (False, error_notes)
                else:
                    print "Password is not a valid format"
                    error_notes['login_password'] = "Password must be at least 8 characters long with at least one capital and number"
                    return (False, error_notes)
        else:
            print "Email format not valid"
            error_notes['login_email'] = "Please enter a valid email"
            return (False, error_notes)

    def update(self, form_data, id):
        print "Updating account"
        error_notes = {}
        for key, value in form_data.items():
            print "arg length=", len(value)
            if len(value) == 0:
                print "Field without value found:", key
                error_notes[key] = "This field cannot be blank"
                return (False, error_notes)

        #Validate first_name
        if User.objects.validateName(form_data['first_name']):
            print "first_name is valid"
        else:
            print "first_name not valid"
            error_notes['first_name'] = "First name must be at least 2 letters and no numbers"
            return (False, error_notes)

        #Validate last_name
        if User.objects.validateName(form_data['last_name']):
            print "last_name is valid"
        else:
            print "last_name not valid"
            error_notes['last_name'] = "last name must be at least 2 letters and no numbers"
            return (False, error_notes)

        if User.objects.validateBirthday(form_data['birthday']):
            print "birthday is valid"
        else:
            print "birthday is not valid"
            error_notes['birthday'] = "Please enter a valid birthday"
            return (False, error_notes)
        # validate email returns tuple (valid, user-object if in DB- False if not) Check to make sure return is (True, False)-
        # email is valid, and not in DB
        user = User.objects.get(id=id)
        email_valid = User.objects.validateEmail(form_data['email'])
        if email_valid[0]:
            print "Email format is valid"
            if not email_valid[1]:
                print "Email in not duplicate"
            else:
                print "Email is already in DB"
                if email_valid[1][0] != user:
                    print "Email is already assigned to a different account"
                    error_notes['email'] = "This email is already assigned to a different account"
                    return (False, error_notes)
        else:
            print "Email format not valid"
            error_notes['email'] = "Please enter a valid email"
            return (False, error_notes)

        if User.objects.validateAnswer(form_data['q_1']):
            print "Q_1 is valid format"
        else:
            print "Q_1 is not valid format"
            error_notes['q_1'] = "Answer must be at least 2 letters long"
            return (False, error_notes)

        if User.objects.validateAnswer(form_data['q_2']):
            print "Q_2 is valid format"
        else:
            print "Q_2 is not valid format"
            error_notes['q_2'] = "Answer must be at least 2 letters long"
            return (False, error_notes)

        if User.objects.validateAnswer(form_data['q_3']):
            print "Q_3 is valid format"
        else:
            print "Q_3 is not valid format"
            error_notes['q_3'] = "Answer must be at least 2 letters long"
            return (False, error_notes)

        print "Update information is Valid"
        questions = Question.objects.filter(user=user)

        question = questions.get(number=1)
        question.answer = form_data['q_1']
        question.save()

        question = questions.get(number=2)
        question.answer = form_data['q_2']
        question.save()

        question = questions.get(number=3)
        question.answer = form_data['q_3']
        question.save()

        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.email = form_data['email']
        user.birthday = form_data['birthday']
        user.save()
        return (True, False)


    def validateName(self, name):
        print "Validating Name:", name
        valid = False
        name_regex = re.compile(r'^[a-zA-Z]{2,}$')
        if name_regex.search(name):
            valid = True
        return valid
    def validateAnswer(self, answer):
        print "Validating Answer:", answer
        valid = False
        a_regex = re.compile(r'^[a-zA-Z0-9]{2,}$')
        if a_regex.search(answer):
            valid = True
        return valid

    def validateEmail(self, email):
        print "Validating Email:", email
        valid = False
        in_DB = False
        email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if email_regex.search(email):
            print "Email format is valid"
            valid = True
            email_check = User.objects.filter(email=email)
            if len(email_check) > 0:
                print "Email in DB"
                in_DB = email_check
        return (valid, in_DB)

    def validateBirthday(self, b_day):
        print "Validating Birthday"
        try:
            #Check to make sure b_day is valid format
            time.strptime(b_day, '%Y-%m-%d')
            #check that the date is not greater than or equal to current date
            now_date = time.strftime('%Y-%m-%d')
            print "b_day", b_day
            print "now_date", now_date
            if b_day <= now_date:
                print "Birthday is valid"
                return True
            else:
                print "Birthday must be before current date"
                return False
        except ValueError:
            print "Invalid date format"
            return False

    def validatePassword(self, pass1, pass2):
        print "Validating Password:", pass1, pass2
        valid = False
        match = False
        password_regex = re.compile(r'(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]{8,}')
        if password_regex.search(pass1):
            print "Password is valid format"
            valid = True
            if pass1 == pass2:
                print "Passwords match"
                match = True
        return (valid, match)

    #This function is used to prevent 'JSON serializable errors' by un-packing the needed information
    #from a query object into a standard dictionary.
    def loginUser(self, user):
        new_obj = {
            'id' : user.id,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'birthday' : user.birthday.isoformat(),
        }
        return new_obj

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Question(models.Model):
    user = models.ForeignKey('User')
    number = models.IntegerField()
    question = models.CharField(max_length=55)
    answer = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
