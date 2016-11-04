class Animal(object):
    def __init__(self, name):
        self.name = name
        self.health = 100
    def walk(self):
        self.health -= 1
        if self.health <= 0:
            print "You walked yourself to death!"
            self.health = 0
        return self

    def run(self):
        self.health -= 5
        if self.health <= 0:
            print "You ran yourself to death!"
            self.health = 0
        return self

    def display_health(self):
        print "{}'s health is {}".format(self.name, self.health)

class Dog(Animal):
    def __init__(self, name):
        super(Dog, self).__init__(name)
        self.health = 150

    def pet(self):
        self.health += 5
        return self

class Dragon(Animal):
    def __init__(self, name):
        super(Dragon, self).__init__(name)
        self.health = 170

    def fly(self):
        self.health -= 10
        return self
    def display_health(self):
        print "\nThis is a Dragon!"
        super(Dragon, self).display_health()

kona = Dog('Kona')
kona.walk().walk().walk().run().run().pet().display_health()

puff = Dragon('Puff')
puff.walk().walk().walk().run().run().fly().display_health()

fluffy = Animal('fluffy')
#fluffy.pet()
#fluffy.fly()
