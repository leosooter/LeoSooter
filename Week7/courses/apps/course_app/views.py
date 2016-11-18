from django.shortcuts import render

from django.shortcuts import render, redirect
from . import models

def index(request, error='0'):
    print "Index route"
    #Testing a method of displaying errors based on url parameters rather than using session
    #The error_list could be expanded to include more errors as needed
    error_list = ['','Please enter a course name']
    #Change error arg to integer
    error = int(error)
    courses = models.Course.objects.all()
    for course in courses:
        print course.description
    context = {
        'courses' : courses,
        'error' : error_list[error],
    }
    return render(request, 'course_app/index.html', context)

def new(request):
    #Creates a new record from the form
    print "New route"
    if request.method == 'POST':
        #Check to make sure the course at least has a name- blank description is accepted
        if len(request.POST['name']):
            print "Post Method"
            name = request.POST['name']
            description = request.POST['description']

            new_description = models.Description.objects.create(content=description)
            new_description.save()
            new_course = models.Course.objects.create(name=name, description=new_description)
            new_course.save()
            print new_course.id
        else:
            #If the name-field is blank: return to index with an error in the url
            return redirect('/1')
    else:
        print "Invalid request method"

    return redirect('/')
#I used the same route to both display the "are you sure you want to delete" template-
#with a GET route and to delete the record with a POST route
def destroy(request, id):
    print "Destroy route. Id =", id
    course = models.Course.objects.get(pk=id)
    #Post route processes delete form from delete.html template
    if request.method == 'POST':
        print "Post method"
        description = course.description
        course.delete()
        description.delete()
        return redirect('/')
    else:
    #Get route displays the "are you sure you want to delete" delete.html template
        print "Get method"
        context = {
            'name' : course.name,
            'description' : course.description.content,
            'id' : id,
        }
        return render(request, 'course_app/delete.html', context)
