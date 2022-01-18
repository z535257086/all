from pynput.mouse import Listener
import paramiko
from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.text = Label(self, text='ip: ')
        self.text.pack(side=LEFT)
        self.valueInput = Entry(self)
        self.valueInput.pack(side=LEFT)
        self.alertButton = Button(self, text='安装', command=self.remotConnect)
        self.alertButton.pack(side=RIGHT)

    def remotConnect(self):
        ip = '10.130.107.11'
        port = 2222
        user = 'yuantu'
        password = 'yuantu'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password, timeout=10)
        messagebox.showinfo('Message', '服务器连接成功')
        # stdout 为正确输出，stderr为错误输出
        stdin, stdout, stderr = ssh.exec_command(f"cd /opt/html/platform-tools/;sh install.sh {self.valueInput.get()}", get_pty=True)
        for line in stdout:
            messagebox.showinfo('Message', line.strip('\n'))
        ssh.close()

app = Application()
# 设置窗口标题:
app.master.title('自动安装')
# 主消息循环:
app.mainloop()