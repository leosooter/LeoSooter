letter_array = ['C','D','F','G','H','J','K','L']
#I did not implement the self.tail attribute. While I can see how it would provide
#some help- especialy on the reverse function- it seems like it would be more useful
#on a double linked list
class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

class SinglyLinkedList(object):
    def __init__(self):
        self.head = None

    def print_all_vals(self):
        print "Printing Values"
        runner = self.head
        print runner.value
        while runner.next != None:
            print runner.next.value
            runner = runner.next

    def add_back(self, val):
        runner = self.head
        while runner.next != None:
            runner = runner.next
        runner.next = Node(val)
        print "Added value", runner.next.value, "to back"

    def add_front(self, val):
        temp = self.head
        self.head = Node(val)
        self.head.next = temp
        print "Added value", self.head.value, "to front"

    def insert_before(self, nextval, val):
        # if self.head.value == nextval:
        #     print "nextval is head"
        #     self.add_front(val)
        # else:
        runner = self.head
        while runner:
            if runner.next.value == nextval:
                print "inserting",val,"before",runner.value
                temp = runner.next
                runner.next = Node(val)
                runner.next.next = temp
                return True
            else:
                trailer = runner
                runner = runner.next
        print "Value not in list"
        return False


    def insert_after(self, preval, val):
        trailer = self.head
        while trailer.value != preval:
            trailer = trailer.next
        if trailer.next == None:
            print "preval is tail"
            self.add_back(val)
        else:
            print "inserting",val,"after",trailer.value
            runner = trailer.next
            trailer.next = Node(val)
            trailer.next.next = runner

    def reverse_list(self):
        if self.head.next == None:
            print "List is one Node long and cannot be reversed"
        else:
            new_head = None
            runner = self.head
            while runner.next != None:
                while runner.next != None:
                    trailer = runner
                    runner = runner.next
                print "Value at end is", runner.value
                if new_head == None:
                    new_head = runner
                trailer.next = None
                runner.next = trailer
                runner = self.head
            self.head = new_head


list = SinglyLinkedList()
list.head = Node('B')

for letter in letter_array:
    list.add_back(letter)

# list.add_front('A')
list.print_all_vals()
list.insert_before('B', 'I')
list.print_all_vals()
# list.insert_after('D','E')
# list.print_all_vals()
#
# list.reverse_list()
# list.print_all_vals()
