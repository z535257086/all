class Student(object):


    # 方法名与实例变量不能重名
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


s = Student()
s.name = "牛逼"
print(s.name)
# print(s)