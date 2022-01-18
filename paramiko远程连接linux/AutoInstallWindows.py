# coding=gbk

from pynput.mouse import Listener
import paramiko
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox as messagebox
import os
from paramikoԶ������linux.excel import e_controller as e
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
    # 0 ���� 1 ��װ 2ж�� 3�رշ�������
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
            print(f"{self.ip}----���ڰ�װ")
            if self.count == 1:
                po = os.popen(self.one_install)
            else:
                po = os.popen(self.install.format(self.ip, self.ip))
            result = po.buffer.read().decode('utf-8')
            if 'Success' in result:
                print(f"{self.ip}----��װ�ɹ�")
            else:
                print(f"{self.ip}----��װʧ��")
        elif self.install_or_uninstall == 2:
            print(f"{self.ip}----����ж��")
            if self.count == 1:
                po = os.popen(self.one_uninstall)
            else:
                po = os.popen(self.uninastall.format(self.ip))
            result = po.buffer.read().decode('utf-8')
            if 'Success' in result:
                print(f"{self.ip}----ж�سɹ�")
            else:
                print(f"{self.ip}----ж��ʧ��")
        elif self.install_or_uninstall == 3:
            print(f"{self.ip}----���ڹر�����")
            os.popen(self.close_connect.format(self.ip))
            print(f"{self.ip}----�����ѹر�")
        elif self.install_or_uninstall == 0:
            ip_result = os.popen(f"ping -n 1 {self.ip}")
            result = str(ip_result.read())
            if "��ʱ" in result or "�޷�����" in result or "������" in result:
                # if ip_result == 1:
                print(f'{self.ip}----ping��ͨ')
                self.if_connect[self.ip] = False
            else:
                print(f"{self.ip}----��������")
                po = os.popen(self.connect.format(self.ip))
                result = po.buffer.read().decode('utf-8')
                if 'already' in result or 'susscessfully' in result or 'connected' in result:
                    print(f"{self.ip}----���ӳɹ�")
                    self.if_connect[self.ip] = True
                else:
                    self.if_connect[self.ip] = False
                    print(f"{self.ip}----����ʧ��:", result)
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
        self.alertButton = Button(self, text='�ر�����', command=self.close_connect)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='ж��', command=self.uninstall)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='��װ', command=self.remotConnect)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='�����豸', command=self.connect)
        self.alertButton.pack(side=RIGHT)
        self.alertButton = Button(self, text='ѡ���ļ�', command=self.upload_file)
        self.alertButton.pack(side=RIGHT)

    def common(self, install_or_uninstall):
        self.ip = self.valueInput.get()
        if self.ip == "" and (self.selectFile == '' or self.ip_list == []):
            messagebox.showinfo('��ʾ', '������ip')
        elif self.selectFile == '' and self.ip != '':
            self.ip = self.valueInput.get()
            if Thread.if_connect.get(self.ip, False) is True:
                thread = Thread(self.ip)
                thread.install_or_uninstall = install_or_uninstall
                thread.sem.acquire()
                thread.start()
            else:
                print(f"{self.ip}δ����------��������")
        elif self.selectFile != '' and self.ip != '':
            self.ip = self.valueInput.get()
            if Thread.if_connect.get(self.ip, False) is True:
                thread = Thread(self.ip)
                thread.install_or_uninstall = install_or_uninstall
                thread.sem.acquire()
                thread.start()
            else:
                print(f"{self.ip}δ����------��������")
        else:
            for ip in self.ip_list:
                if Thread.if_connect.get(ip, False) is True:
                    thread = Thread(ip, 2)
                    thread.install_or_uninstall = install_or_uninstall
                    thread.sem.acquire()
                    thread.start()
                else:
                    print(f'{ip}�豸δ����,���������豸')

    def close_connect(self):
        self.common(3)

    def connect(self):
        self.ip = self.valueInput.get()
        if self.selectFile == '' or len(self.ip_list) == 0:
            if self.ip == "":
                messagebox.showinfo('��ʾ', '������ip')
            else:
                # adb ��װ apk
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
                print(result, "����ʧ��")
                for i in result:
                    if i in self.ip_list:
                        self.ip_list.remove(i)
                        Thread.if_connect.pop(i)
                print("����ʧ�ܵ�ip��ɾ������ֻ��������ip���в�������Ҫ��������ip������ѡ���ļ�\n�����ӵ�ipΪ", self.ip_list, ',����', len(self.ip_list), '��ip���ӳɹ�')
            result.clear()

    def upload_file(self):
        self.selectFile = tkinter.filedialog.askopenfilename(title='ѡ���ļ�')
        if self.selectFile != "":
            messagebox.showinfo('��ʾ', f'�ļ�����{self.selectFile}������ȡ�ɹ�')
            table = e(self.selectFile, 0)
            self.ip_list = [table.get_value(i, 0) for i in range(0, table.get_nrows())]
            print("��ȡ����ip��ַΪ��", self.ip_list)

    def uninstall(self):
        self.common(2)

    def remotConnect(self):
        self.common(1)


app = Application()
# ���ô��ڱ���:
app.master.title('�Զ���װ')
# ����Ϣѭ��:
app.mainloop()
