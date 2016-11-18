from django.shortcuts import render, redirect
from django.contrib import messages
from . import models

def index(request):
    print "Index Route"
    return render(request, 'email_validation/index.html')

def success(request):
    print "Success Route"
    emails = models.Email.objects.all()
    context = {'emails' : emails }
    return render(request, 'email_validation/success.html', context)

def new(request):
    if request.method == 'POST':
        email = str(request.POST['email'])
        #Returns tuple ((email is valid):True/False, note to be displayed)
        validation = models.Email.objects.validate(email)
        if validation[0]:
            new_email = models.Email.objects.create(email=email)
            new_email.save()
            messages.success(request, validation[1])
            return redirect('/success')
        else:
            messages.error(request, validation[1])
            return redirect('/')
    else:
        print "Invalid request method"
        return redirect('/')

def destroy(request, id):
    print "Destroy route, ID =", id
    if request.method == 'POST':
        #Check to ensure that one and only one record exists without breaking on failure
        delete_email = models.Email.objects.filter(id=id)
        if len(delete_email) == 1:
            delete_email[0].delete()
        elif len(delete_email) == 0:
            print "Email to delete not found in records"
        else:
            print "Duplicate emails found in records"
    else:
        print "Invalid request method"

    return redirect('/success')


# Create your views here.
