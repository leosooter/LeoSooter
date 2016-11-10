from django.shortcuts import render, redirect

def index(request):
    print "Index Route"
    return render(request, 'dis_ninja/index.html')

def ninjas(request):
    print "Ninjas Route"
    return render(request, 'dis_ninja/ninjas.html')

def show(request, color):
    print "Show Route"
    if color in ('blue', 'red', 'orange', 'purple'):
        context = {
            'color' : color,
        }
    else:
        context = {
            'color' : 'fox'
        }
    return render(request, 'dis_ninja/show.html', context)
