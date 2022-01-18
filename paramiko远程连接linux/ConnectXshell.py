import paramiko
# import re
# from time import sleep
#
#
# class Linux(object):
#     # 初始化linux主机
#     def __init__(self, ip, username, password, timeout=30):
#         self.ip = ip
#         self.username = username
#         self.password = password
#         self.timeout = timeout
#         # transport   chanel
#         self.t = ''
#         self.chan = ''
#         # 重试连接次数
#         self.try_times = 3
#
#     def connect(self):
#         while True:
#             try:
#                 self.t = paramiko.Transport(sock=(self.ip, 22))


class ConnectShell:
    def remotConnect(self, cmd):
        ip = "10.32.10.3"
        port = 22
        user = 'yuantu'
        password = 'yuantu'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password, timeout=10)
        # stdout 为正确输出，stderr为错误输出
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        for line in stdout:
            print(line.strip('\n'))
        for line in stderr:
            print(line)
        ssh.close()

if __name__ == '__main__':
    linux = ConnectShell()
    cmd = "cd /opt/tomcat-queue/logs;tail -10f queue-job.log.2021-12-26"
    linux.remotConnect(cmd)