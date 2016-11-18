from __future__ import unicode_literals
from django.db import models
import re

class Email_Manager(models.Manager):
    def validate(self, email):
        print "Email =", email, "///////////////////////////////////////////////"
        print type(email)
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        valid = False
        note = ""
        print "Checking that input has value and is string"
        if len(email) and type(email) is str:
            print "Check for valid format"
            if email_regex.search(email):
                print "Format is valid"
                print "Check DB to see if duplicate"
                email_check = Email.objects.filter(email=email)
                if len(email_check) == 0:
                    print "No duplicate in DB"
                    print "Email is valid"
                    valid = True
                    note = "The email address you entered: {}, is a VALID address. Thank you!".format(email)
                else:
                    print "Email already in DB"
                    note = "The email you entered is already in our records"
            else:
                print "Invalid Format"
                note = "Email must be a valid format"
        else:
            print "No value or value is not a string"
            note = "Please enter a valid email"

        return (valid, note)

class Email(models.Model):
    email = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Email_Manager()
