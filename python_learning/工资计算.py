from abc import ABCMeta,abstractmethod

class Employee(object,metaclass=ABCMeta):
    def __init__(self,name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def salary(self):
        pass

class Manage(Employee):
    def salary(self):
        return 25000

class cxy(Employee):
    def __init__(self,name,hour = 0):
        super().__init__(name)
        self._hour = hour

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self,hour):
        self._hour = hour

    def salary(self):
        return 150*self._hour


class sales(Employee):
    def __init__(self,name,ticheng = 0):
        super().__init__(name)
        self._ticheng = ticheng

    @property
    def ticheng(self):
        return self._ticheng

    @ticheng.setter
    def ticheng(self,ticheng):
        self._ticheng = ticheng

    def salary(self):
        return 1200.0+0.05*self._ticheng

def main():
    emps = [
        Manage('经理1'),Manage('经理2'),Manage('经理3'),
        sales('销售1'),sales('销售2'),sales('销售3'),
        cxy('程序员1'),cxy('程序员2'),cxy('程序员3')
    ]
    for emp in emps:
        if isinstance(emp,Manage):
            print(f'{emp.name}的工资为{emp.salary()}')
        elif isinstance(emp,sales):
            emp.ticheng = float(input("输入%s销售额：" % emp.name))
            print(f'{emp.name}的工资为{emp.salary()}')
        else:
            emp.hour = int(input("输入%s工作时长:" % emp.name))
            print(f'{emp.name}的工资为{emp.salary()}')

if __name__ == '__main__':
    main()