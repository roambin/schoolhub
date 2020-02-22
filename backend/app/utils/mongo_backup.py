from public import config
import paramiko
import datetime


def ssh(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.HOST, 22, config.SERVER_USER, config.SERVER_PASSWD)
    stdin, stdout, stderr = ssh.exec_command(command)
    outmsg, errmsg = stdout.read(), stderr.read()
    ssh.close()
    if errmsg:
        return errmsg.decode(), False
    return outmsg.decode(), True


def list_file():
    msg, stat = ssh('ls ' + config.MONGO_DUMP_PATH)
    if not stat:
        return None
    if not msg:
        return []
    return msg[:-1].split('\n')


def ssh_bool(command):
    msg, stat = ssh(command)
    if not stat:
        print(msg)
        return False
    return True


def delete(filename):
    return ssh_bool('rm -rf ' + config.MONGO_DUMP_PATH + filename)


def dump(filename=None):
    if not filename:
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    ssh("mongodump -h "+config.MONGO_HOST+" -u "+config.MONGO_USER+" -p "+config.MONGO_PASSWD+" -d schoolhub -o "+config.MONGO_DUMP_PATH+"" + filename)
    return ssh_bool('ls ' + config.MONGO_DUMP_PATH + filename)


def restore(filename):
    msg, stat = ssh("mongorestore -h "+config.MONGO_HOST+" -u "+config.MONGO_USER+" -p "+config.MONGO_PASSWD+" --drop "+config.MONGO_DUMP_PATH+"" + filename)
    return msg[msg.rindex('\t')+1:-1] == 'done'


# print(list_file())
# print(dump('1'))
# print(restore())
# print(delete('1'))
