from socket import *
from threading import Thread
from time import sleep
from urllib import parse,request
import time
import json
from sql import *


Host,Port = 'localhost', 7007 

cache_time = {}
cache_data = {}

def validateDate(str):
    data = json.loads(str)
    if data['resultcode'] != '200':
        return False
    return True

def getData(city):
    if city in cache_time.keys():
        if cache_time[city] + 600 >= time.time():
            return cache_data[city]
    url = 'http://v.juhe.cn/weather/index?'
    parm = {'format':'1','cityname':rec, 'key':'7dfab88a535f36c04d886aba7cad8e75'}
    parm = parse.urlencode(parm)
    url = url + parm
    res = request.urlopen(url).read().decode('utf-8')
    if validateDate(res) is True:
        cache_time[city] = time.time()
        cache_data[city] = res
        return True
    return False



def handle_request(connection, addr):
    info = connection.recv(1024)
    if len(info) > 0:
        city = str(info.decode())

        connection.sendall('okokok'.encode('utf-8'))
        
    else:
        print('client was closed')
    connection.close()


def Start():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((Host, Port))
    sock.listen(10)
    try:
        while True:
            connection, address = sock.accept()
            client = Thread(target=handle_request, args=(connection, address))
            client.start()
    finally:
        sock.close()

if __name__ == '__main__':
    SQL = sqlFactory('root', 'yiersan321', 'test')
    val = []
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    val.append('\'xian\'')
    SQL.insertData(val)
    SQL.close()