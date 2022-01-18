from time import sleep
from threading import Thread, Lock


class Account(object):

    def __init__(self):
        self._balance = 0
        self._lock = Lock()

    def deposit(self, money):
        # 先获取锁才能执行后续的代码
        self._lock.acquire()
        try:
            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
        finally:
            # 在finally中执行释放锁的操作保证正常异常锁都能释放
            self._lock.release()

    @property
    def balance(self):
        return self._balance


class AddMoneyThread(Thread):

    def __init__(self, account, money):
        super().__init__()
        self._account = account
        self._money = money

    def run(self):
        self._account.deposit(self._money)


def main():
    account = Account()
    threads = []
    for _ in range(100):
        t = AddMoneyThread(account, 1)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print('账户余额为: ￥%d元' % account.balance)


if __name__ == '__main__':
    main()













# from random import randint
# from threading import Thread
# from time import time, sleep
#
#
# class DownloadTask(Thread):
#
#     def __init__(self, filename):
#         super().__init__()
#         self._filename = filename
#
#     def run(self):
#         print('开始下载%s...' % self._filename)
#         time_to_download = randint(5, 10)
#         sleep(time_to_download)
#         print('%s下载完成! 耗费了%d秒' % (self._filename, time_to_download))
#
#
# def main():
#     start = time()
#     t1 = DownloadTask('Python从入门到住院.pdf')
#     t1.start()
#     t2 = DownloadTask('Peking Hot.avi')
#     t2.start()
#     t1.join(5)
#     t2.join(5)
#     end = time()
#     print('总共耗费了%.2f秒.' % (end - start))
#
#
# if __name__ == '__main__':
#     main()