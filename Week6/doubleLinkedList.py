letter_array = ['C','D','F','G','H','J','K','L']
class Node(object):
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class double_link_list(object):
    def __init__(self):
        self.head = None
        self.tail = None

    def print_all_vals(self):
        runner = self.head
        print "\nList Values:"
        print runner.value
        while runner != self.tail:
            runner = runner.next
            print runner.value


    def add_back(self, val):
        print "adding", val, "to back"
        self.tail.next = Node(val)
        self.tail.next.prev = self.tail
        self.tail = self.tail.next

    def add_front(self, val):
        print "adding", val, "to front"
        self.head.prev = Node(val)
        self.head.prev.next = self.head
        self.head = self.head.prev

    def insert_before(self, nextval, val):
        if self.head.value == nextval:
            print "Value to insert before is head"
            self.add_front(val)
        else:
            runner = self.tail
            while runner.value != nextval and runner != self.head:
                runner = runner.prev
            if runner == self.head:
                print "Value to insert before not found in list"
            else:
                print "Inserting", val, "before", runner.value
                temp = runner.prev
                runner.prev = Node(val)
                runner.prev.next = runner
                runner.prev.prev = temp
                temp.next = runner.prev

    def insert_after(self, preval, val):
        if self.tail.value == preval:
            print "Value to insert after is tail"
            self.add_back(val)
        else:
            runner = self.head
            while runner.value != preval and runner != self.tail:
                runner = runner.next
            if runner == self.tail:
                print "Value to insert after not found in list"
            else:
                print "Inserting", val, "after", runner.value
                temp = runner.next
                runner.next = Node(val)
                runner.next.prev = runner
                runner.next.next = temp
                temp.prev = runner.next





list = double_link_list()
list.head = Node('A')
list.tail = list.head

for letter in letter_array:
    list.add_back(letter)

list.print_all_vals()

list.insert_before('F', 'E')
list.insert_after('H', 'I')
list.insert_after('A', 'B')
list.print_all_vals()
