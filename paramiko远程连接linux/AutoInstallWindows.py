# coding=gbk

from pynput.mouse import Listener
import paramiko
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox as messagebox
import os
from paramiko远程连接linux.excel import e_controller as e
import threading
import queue
from threading import Condition


class CountDownLatch:
    count = 0

    def __init__(self):
        self.condition = Condition()

    def add_count(self):
        self.count += 1

    def wait(self):
        try:
            self.condition.acquire()
            while self.count > 0:
                self.condition.wait()
        finally:
            self.condition.release()

    def countDown(self):
        try:
            self.condition.acquire()
            self.count -= 1
            self.condition.notifyAll()
        finally:
            self.condition.release()

    def getCount(self):
        return self.count


class Thread(threading.Thread):
    workQueue = queue.Queue(3)
    # 0 连接 1 安装 2卸载 3关闭服务连接
    install_or_uninstall = 0
    if_connect = {}
    sem = threading.Semaphore(3)
    latch = CountDownLatch()

    def __init__(self, ip, count=1):
        threading.Thread.__init__(self)
        self.ip = ip
        self.count = count
        self.connect = r"cd ../adb && adb connect {}"
        self.one_install = r"cd ../adb" \
                           r"&& adb install zhenjian.apk " \
                           r"&& adb shell am start -n com.yuantu.zhenjianping/com.yuantu.zhenjianping.MainActivity "
        self.install = r"cd ../adb" \
                       r"&& adb -s {} install zhenjian.apk " \
                       r"&& adb -s {} shell am start -n com.yuantu.zhenjianping/com.yuantu.zhenjianping.MainActivity "
        self.one_uninstall = 'cd ../adb && adb uninstall com.yuantu.zhenjianping'
        self.uninastall = 'cd ../adb && adb -s {} uninstall com.yuantu.zhenjianping'
        self.close_connect = 'cd ../adb && adb kill-server'

    def run(self):
        if self.install_or_uninstall == 1:
            print(f"{self.ip}----正在安装")
            if self.count == 1:
                po = os.popen(self.one_install)
            else:
                po = os.popen(self.install.format(self.ip, self.ip))
            result = po.buffer.read().decode('utf-8')
            if 'Success' in result:
                print(f"{self.ip}----安装成功")
            else:
                print(f"{self.ip}----安装失败")
        elif self.install_or_uninstall == 2:
            print(f"{self.ip}----正在卸载")
            if self.count == 1:
                po = os.popen(self.one_uninstall)
            else:
                po = os.popen(self.uninastall.format(self.ip))
            result = po.buffer.read().decode('utf-8')
            if 'Success' in result:
                print(f"{self.ip}----卸载成功")
            else:
                print(f"{self.ip}----卸载失败")
        elif self.install_or_uninstall == 3:
            print(f"{self.ip}----正在关闭连接")
            os.popen(self.close_connect.format(self.ip))
            print(f"{self.ip}----连接已关闭")
        elif self.install_or_uninstall == 0:
            ip_result = os.popen(f"ping -n 1 {self.ip}")
            result = str(ip_result.read())
            if "超时" in result or "无法访问" in result or "不存在" in result:
                # if ip_result == 1:
                print(f'{self.ip}----ping不通')
                self.if_connect[self.ip] = False
            else:
                print(f"{self.ip}----正在连接")
                po = os.popen(self.connect.format(self.ip))
                result = po.buffer.read().decode('utf-8')
                if 'already' in result or 'susscessfully' in result or 'connected' in result:
                    print(f"{self.ip}----连接成功")
                    self.if_connect[self.ip] = True
                else:
                    self.if_connect[self.ip] = False
                    print(f"{self.ip}----连接失败:", result)
                # print(self.if_connect)
        self.sem.release()
        self.latch.countDown()


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.selectFile = ''
        self.thread_list = []

    def createWidgets(self):
        self.text = Label(self, text='ip: ')
        self.text.pack(side=LEFT)
        self.valueInput = Entry(self)
        self.valueInput.pack(side=LEFT)
        self.alertButton = Button(self, text='关闭连接', command=self.close_connect)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='卸载', command=self.uninstall)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='安装', command=self.remotConnect)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='连接设备', command=self.connect)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='选择文件', command=self.upload_file)
        self.alertButton.pack(side=RIGHT)

    def common(self, install_or_uninstall):
        self.ip = self.valueInput.get()
        if self.ip == "" and (self.selectFile == '' or self.ip_list == []):
            messagebox.showinfo('提示', '请输入ip')
        elif self.selectFile == '' and self.ip != '':
            self.ip = self.valueInput.get()
            if Thread.if_connect.get(self.ip, False) is True:
                thread = Thread(self.ip)
                thread.install_or_uninstall = install_or_uninstall
                thread.sem.acquire()
                thread.start()
            else:
                print(f"{self.ip}未连接------请先连接")
        elif self.selectFile != '' and self.ip != '':
            self.ip = self.valueInput.get()
            if Thread.if_connect.get(self.ip, False) is True:
                thread = Thread(self.ip)
                thread.install_or_uninstall = install_or_uninstall
                thread.sem.acquire()
                thread.start()
            else:
                print(f"{self.ip}未连接------请先连接")
        else:
            for ip in self.ip_list:
                if Thread.if_connect.get(ip, False) is True:
                    thread = Thread(ip, 2)
                    thread.install_or_uninstall = install_or_uninstall
                    thread.sem.acquire()
                    thread.start()
                else:
                    print(f'{ip}设备未连接,请先连接设备')

    def close_connect(self):
        self.common(3)

    def connect(self):
        self.ip = self.valueInput.get()
        if self.selectFile == '' or len(self.ip_list) == 0:
            if self.ip == "":
                messagebox.showinfo('提示', '请输入ip')
            else:
                # adb 安装 apk
                thread = Thread(self.ip)
                thread.install_or_uninstall = 0
                thread.sem.acquire()
                thread.start()
                # os.system(self.cmd.format(ip))
        elif self.selectFile != '' and self.ip != '':
            thread = Thread(self.ip)
            thread.install_or_uninstall = 0
            thread.sem.acquire()
            thread.start()
        else:
            for ip in self.ip_list:
                thread = Thread(ip)
                Thread.latch.add_count()
                thread.install_or_uninstall = 0
                thread.sem.acquire()
                thread.start()
                self.thread_list.append(thread)
            for i in self.thread_list:
                i.join()
            result = [k for k, v in Thread.if_connect.items() if v == FALSE]
            if len(result) != 0:
                print(result, "连接失败")
                for i in result:
                    if i in self.ip_list:
                        self.ip_list.remove(i)
                        Thread.if_connect.pop(i)
                print("连接失败的ip已删除，将只对已连接ip进行操作，需要重新连接ip请重新选择文件\n已连接的ip为", self.ip_list, ',共有', len(self.ip_list), '个ip连接成功')
            result.clear()

    def upload_file(self):
        self.selectFile = tkinter.filedialog.askopenfilename(title='选择文件')
        if self.selectFile != "":
            messagebox.showinfo('提示', f'文件——{self.selectFile}——获取成功')
            table = e(self.selectFile, 0)
            self.ip_list = [table.get_value(i, 0) for i in range(0, table.get_nrows())]
            print("获取到的ip地址为：", self.ip_list)

    def uninstall(self):
        self.common(2)

    def remotConnect(self):
        self.common(1)


app = Application()
# 设置窗口标题:
app.master.title('自动安装')
# 主消息循环:
app.mainloop()
