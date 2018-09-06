from socket import *
from threading import Thread
from time import sleep
from urllib import parse,request
import time
import json
from sql import *


Host,Port = 'localhost', 7007 

cache_time = {}
SQL = sqlFactory('root', 'yiersan321', 'smog')

def validateDate(str):
    data = json.loads(str)
    if data['resultcode'] != '200':
        return False
    return True

def getData(city):
    if city in cache_time.keys():
        if cache_time[city] + 600 >= time.time():
            return SQL.queryData(city)
    url = 'http://v.juhe.cn/weather/index?'
    parm = {'format':'1','cityname':city, 'key':'7dfab88a535f36c04d886aba7cad8e75'}
    parm = parse.urlencode(parm)
    url = url + parm
    print(url)
    res = request.urlopen(url).read().decode('utf-8')
    if validateDate(res) is True:
        val = []
        val.append(city)
        data = json.loads(res)
        data = data['result']

        sk = data['sk']
        val.append(sk['temp'])
        val.append(sk['wind_direction'])
        val.append(sk['wind_strength'])
        val.append(sk['humidity'])
        today = data['today']
        val.append(today['temperature'])
        val.append(today['weather'])
        val.append(today['dressing_advice'])
        val.append(today['uv_index'])

        SQL.insertData(val)
        cache_time[city] = time.time()
        return SQL.queryData(city)
    return False



def handle_request(connection, addr):
    info = connection.recv(1024)
    if len(info) > 0:
        city = str(info.decode())
        ans = getData(city)
        connection.sendall(ans.encode('utf-8'))
        
    else:
        print('client was closed')
    connection.close()


def Start():
    SQL.initTable()
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
        SQL.close()

if __name__ == '__main__':
    Start()
    
    
