class Person(object):
    def __init__(self,name,age):
        self.name =name
        self.age =age

    def __str__(self):
        return "<{} {}>".format(self.name, self.age)


p =Person("小黑",18)
print(p)
p2 = Person("高材生",9000)
print(p2)