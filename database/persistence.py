import shelve

class Person:
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
    def __str__(self):
        return "<{0} => {1}>".format(self.__class__.__name__, self.name)

db = shelve.open('Persons')
daniel = Person('Daniel Garcia', 18, 19)
db['daniel'] = daniel
db.close()