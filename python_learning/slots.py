from types import MethodType


class Student(object):
    def __init__(self, name):
        self.name = name


def set_name(self, name):
    self.name = name


def get_name(self):
    return self.name


# s = Studnet()
# s.set_name = MethodType(set_name, s)
# s.set_name("李四")
# print(s.name)



s = Student("张三")
s2 = Student("王五")
Student.set_name = MethodType(set_name, Student)
Student.get_name = MethodType(get_name, Student)
Student.set_name("李四")
print(s.name)
print(Student.get_name())
print(Student.name)
print(s2.get_name())
