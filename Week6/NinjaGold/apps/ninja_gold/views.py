from django.shortcuts import render, redirect
from random import randint
from datetime import datetime
def index(request):
    print "Index route"
    class Location(object):
        def __init__(self, name, gold_min, gold_max):
            self.name = name.title()
            self.gold_min = gold_min
            self.gold_max = gold_max
            if gold_min < 0:
                self.earns = 'Earns/Takes (0 - {})'.format(gold_max)
            else:
                self.earns = 'Earns ({} - {})'.format(gold_min, gold_max)
            self.img_path = "ninja_gold/images/{}.jpg".format(name)

    farm = Location('farm', 10, 20)
    cave = Location('cave', 5, 10)
    house = Location('house', 2, 5,)
    casino = Location('casino', -50, 50)

    context = {
        'location_list' : [farm, cave, house, casino]
    }
    if 'gold' not in request.session:
        request.session['gold'] = 0

    if 'actions' not in request.session:
        request.session['actions'] = []
    return render(request, 'ninja_gold/index.html', context)

def process(request):
    print "Process route"
    if request.method == 'POST':
        print int(request.POST['gold_min'])
        print int(request.POST['gold_max'])
        amount = randint(int(request.POST['gold_min']), int(request.POST['gold_max']))
        if amount > 0:
            action = {
                'message' : "Earned {} gold from the {}! ({})".format(amount, request.POST['name'], datetime.strftime(datetime.now(), '%c')),
                'class' : "green",
            }
        else:
            action = {
                'message' : "You lost {} gold at the Casino- Ouch! ({})".format(amount, datetime.strftime(datetime.now(), '%c')),
                'class' : "red",
            }

        request.session['gold'] += amount
        request.session['actions'].append(action)
        print amount
    else:
        print "Invalid request method"

    return redirect('/')
