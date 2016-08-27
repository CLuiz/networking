import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/juston/.xssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return
    
#test command
ssh_command('192.168.100.131', 'justin', 'lovesthepython','id')