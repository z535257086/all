# __solts__限定对象只对当前类生效
class Person(object):

    # 限定Person对象只能绑定_name, _age和_gender属性
    __slots__ = ('_name', '_age', '_gender')

    def __init__(self, name, age):
        self._name = name
        self._age = age
        # self._height = height

    @classmethod
    def cm(cls):
        return cls("王大锤",20)

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def height(self):
        return self._height

    @age.setter
    def age(self, age):
        self._age = age

    # @height.setter
    # def height(self, height):
    #     self._height = height

    def play(self):
        if self._age <= 16:
            print('%s正在玩飞行棋.' % self._name)
        else:
            print('%s正在玩斗地主.' % self._name)


def main():
    person = Person.cm()
    person.play()
    person._gender = '男'
    # AttributeError: 'Person' object has no attribute '_is_gay'
    # person._is_gay = True
    print(person._gender)


if __name__ == "__main__":
    main()














# getter 和 setter
# class Person:
#
#     def __init__(self, name, age):
#         self.__name = name
#         self.__age = age
#
#     @property
#     def name(self):
#         return self.__name
#
#     @property
#     def age(self):
#         return self.__age
#
#     @age.setter
#     def age(self, age):
#         self.__age = age
#
#     @name.setter
#     def name(self, name):
#         self.__name = name
#
#     def play(self):
#         if self.__age <= 16:
#             print('%s正在玩飞行棋.' % self.__name)
#         else:
#             print('%s正在玩斗地主.' % self.__name)
#
#
# def main():
#     person = Person('王大锤', 12)
#     person.play()
#     person.age = 24
#     print(person.name)
#     person.play()
#     person.name = '白元芳'  # AttributeError: can't set attribute
#     person.play()

# class Test:
#
#     def __init__(self, foo):
#         self._foo = foo
#
#     # def __bar(self):
#     #     print(self.__foo)
#     #     print('__bar')
#
#
# def main():
#     test = Test('hello')
#     # AttributeError: 'Test' object has no attribute '__bar'
#     # test.__bar()
#     # AttributeError: 'Test' object has no attribute '__foo'
#     print(test._foo)


# if __name__ == "__main__":
#     main()

#
# if __name__ == '__main__':
#     main()