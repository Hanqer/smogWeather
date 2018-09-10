from socket import *
from threading import Thread
from time import sleep
from urllib import parse,request
import time
import json
from sql import *


Host,Port = 'localhost', 7007 

cache_time = {}
#SQL = sqlFactory('root', 'yiersan321', 'smog')

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
    #Start()
    #a994e1e0da944ee3a1462c641aa1980a

    city = '西安'
    local = '长安区'
    url = 'https://free-api.heweather.com/s6/weather/now?'
    temp = local+','+city
    parm = {'location':temp, 'key':'a994e1e0da944ee3a1462c641aa1980a'}
    parm = parse.urlencode(parm)
    url = url + parm
    #res = request.urlopen(url).read().decode('utf-8')
    res = '{"HeWeather6":[{"basic":{"cid":"CN101110102","location":"长安","parent_city":"西安","admin_area":"陕西","cnty":"中国","lat":"34.15709686","lon":"108.94158173","tz":"+8.00"},"update":{"loc":"2018-09-10 18:46","utc":"2018-09-10 10:46"},"status":"ok","now":{"cloud":"0","cond_code":"101","cond_txt":"多云","fl":"26","hum":"48","pcpn":"0.0","pres":"1013","tmp":"25","vis":"35","wind_deg":"181","wind_dir":"南风","wind_sc":"1","wind_spd":"2"}}]}'

    data = json.loads(res)
    val = {}
    val['city'] = city+'-'+local
    if data['HeWeather6'][0]['status'] == 'ok':
        now = data['HeWeather6'][0]['now']
        val['sk_temp'] = now['tmp']
        val['sk_weather'] = now['cond_txt']
        val['wind_direction'] = now['wind_dir']
        val['wind_strength'] = now['wind_sc']
        val['humidity'] = now['hum']+'%'
        print(val)

    parm = {'location':city, 'key':'a994e1e0da944ee3a1462c641aa1980a'}
    parm = parse.urlencode(parm)
    url = 'https://free-api.heweather.com/s6/air/now?' + parm
    #res = request.urlopen(url).read().decode('utf-8')
    res = '{"HeWeather6":[{"basic":{"cid":"CN101110101","location":"西安","parent_city":"西安","admin_area":"陕西","cnty":"中国","lat":"34.26316071","lon":"108.94802094","tz":"+8.00"},"update":{"loc":"2018-09-10 19:46","utc":"2018-09-10 11:46"},"status":"ok","air_now_city":{"aqi":"33","qlty":"优","main":"-","pm25":"14","pm10":"33","no2":"23","so2":"8","co":"0.7","o3":"104","pub_time":"2018-09-10 19:00"},"air_now_station":[{"air_sta":"高压开关厂","aqi":"45","asid":"CNA1462","co":"0.6","lat":"34.2749","lon":"108.882","main":"-","no2":"36","o3":"98","pm10":"45","pm25":"10","pub_time":"2018-09-10 19:00","qlty":"优","so2":"7"},{"air_sta":"兴庆小区","aqi":"36","asid":"CNA1463","co":"0.9","lat":"34.2629","lon":"108.993","main":"-","no2":"13","o3":"110","pm10":"36","pm25":"16","pub_time":"2018-09-10 19:00","qlty":"优","so2":"10"},{"air_sta":"纺织城","aqi":"36","asid":"CNA1464","co":"0.8","lat":"34.2572","lon":"109.06","main":"-","no2":"25","o3":"96","pm10":"36","pm25":"19","pub_time":"2018-09-10 19:00","qlty":"优","so2":"14"},{"air_sta":"小寨","aqi":"31","asid":"CNA1465","co":"0.6","lat":"34.2324","lon":"108.94","main":"-","no2":"24","o3":"97","pm10":"16","pm25":"9","pub_time":"2018-09-10 19:00","qlty":"优","so2":"8"},{"air_sta":"市人民体育场","aqi":"34","asid":"CNA1466","co":"0.6","lat":"34.2713","lon":"108.954","main":"-","no2":"31","o3":"92","pm10":"34","pm25":"15","pub_time":"2018-09-10 19:00","qlty":"优","so2":"10"},{"air_sta":"高新西区","aqi":"30","asid":"CNA1467","co":"0.6","lat":"34.2303","lon":"108.883","main":"-","no2":"21","o3":"79","pm10":"30","pm25":"15","pub_time":"2018-09-10 19:00","qlty":"优","so2":"6"},{"air_sta":"经开区","aqi":"34","asid":"CNA1468","co":"0.6","lat":"34.3474","lon":"108.935","main":"-","no2":"22","o3":"103","pm10":"34","pm25":"8","pub_time":"2018-09-10 19:00","qlty":"优","so2":"6"},{"air_sta":"长安区","aqi":"29","asid":"CNA1469","co":"0.7","lat":"34.1546","lon":"108.906","main":"-","no2":"18","o3":"92","pm10":"24","pm25":"6","pub_time":"2018-09-10 19:00","qlty":"优","so2":"5"},{"air_sta":"阎良区","aqi":"46","asid":"CNA1470","co":"0.8","lat":"34.6575","lon":"109.2","main":"-","no2":"24","o3":"142","pm10":"46","pm25":"29","pub_time":"2018-09-10 19:00","qlty":"优","so2":"9"},{"air_sta":"临潼区","aqi":"34","asid":"CNA1471","co":"0.4","lat":"34.3731","lon":"109.2186","main":"-","no2":"19","o3":"108","pm10":"24","pm25":"14","pub_time":"2018-09-10 19:00","qlty":"优","so2":"8"},{"air_sta":"草滩","aqi":"49","asid":"CNA1472","co":"0.8","lat":"34.378","lon":"108.869","main":"-","no2":"17","o3":"133","pm10":"49","pm25":"12","pub_time":"2018-09-10 19:00","qlty":"优","so2":"7"},{"air_sta":"曲江文化产业集团","aqi":"29","asid":"CNA1473","co":"0.5","lat":"34.1978","lon":"108.985","main":"-","no2":"20","o3":"92","pm10":"23","pm25":"10","pub_time":"2018-09-10 19:00","qlty":"优","so2":"4"},{"air_sta":"广运潭","aqi":"35","asid":"CNA1474","co":"0.8","lat":"34.3274","lon":"109.043","main":"-","no2":"20","o3":"110","pm10":"23","pm25":"14","pub_time":"2018-09-10 19:00","qlty":"优","so2":"6"}]}]}'
    if data['HeWeather6'][0]['status'] == 'ok':
        now = data['HeWeather6'][0]['air_now_city']
        val['qlty'] = now['qlty']
        val['pm25'] = now['pm25']
        val['qlty_index'] = now['aqi']

    parm = {'location':temp, 'key':'a994e1e0da944ee3a1462c641aa1980a'}
    parm = parse.urlencode(parm)
    url = 'https://free-api.heweather.com/s6/weather/lifestyle?' + parm
    #res = request.urlopen(url).read().decode('utf-8')
    res = '{"HeWeather6":[{"basic":{"cid":"CN101110102","location":"长安","parent_city":"西安","admin_area":"陕西","cnty":"中国","lat":"34.15709686","lon":"108.94158173","tz":"+8.00"},"update":{"loc":"2018-09-10 19:46","utc":"2018-09-10 11:46"},"status":"ok","lifestyle":[{"type":"comf","brf":"较不舒适","txt":"今天夜间天气晴好，也会使您感到有些热，不很舒适。"},{"type":"drsg","brf":"炎热","txt":"天气炎热，建议着短衫、短裙、短裤、薄型T恤衫等清凉夏季服装。"},{"type":"flu","brf":"少发","txt":"各项气象条件适宜，发生感冒机率较低。但请避免长期处于空调房间中，以防感冒。"},{"type":"sport","brf":"较适宜","txt":"天气较好，但由于风力较大，推荐您在室内进行低强度运动，若在户外运动请注意避风。"},{"type":"trav","brf":"适宜","txt":"天气较好，是个好天气哦。稍热但是风大，能缓解炎热的感觉，适宜旅游，可不要错过机会呦！"},{"type":"uv","brf":"强","txt":"紫外线辐射强，建议涂擦SPF20左右、PA++的防晒护肤品。避免在10点至14点暴露于日光下。"},{"type":"cw","brf":"较适宜","txt":"较适宜洗车，未来一天无雨，风力较小，擦洗一新的汽车至少能保持一天。"},{"type":"air","brf":"良","txt":"气象条件有利于空气污染物稀释、扩散和清除，可在室外正常活动。"}]}]}'
    if data['HeWeather6'][0]['status'] == 'ok':
        now = data['HeWeather6'][0]['lifestyle']
        for life in now:
            if life['type'] == 'comf':
                val['comf'] = life['txt']
            if life['type'] == 'drsg':
                val['drsg'] = life['txt']
            if life['type'] == 'sport':
                val['sport'] = life['txt']
            if life['type'] == 'tral':
                val['tral'] = life['txt']
            if life['type'] == 'uv':
                val['uv'] = life['txt']
    
    parm = {'location':temp, 'key':'a994e1e0da944ee3a1462c641aa1980a'}
    parm = parse.urlencode(parm)
    url = 'https://free-api.heweather.com/s6/weather/forecast?' + parm
    #res = request.urlopen(url).read().decode('utf-8')
    res = '{"HeWeather6":[{"basic":{"cid":"CN101110102","location":"长安","parent_city":"西安","admin_area":"陕西","cnty":"中国","lat":"34.15709686","lon":"108.94158173","tz":"+8.00"},"update":{"loc":"2018-09-10 19:46","utc":"2018-09-10 11:46"},"status":"ok","daily_forecast":[{"cond_code_d":"101","cond_code_n":"101","cond_txt_d":"多云","cond_txt_n":"多云","date":"2018-09-10","hum":"40","mr":"06:37","ms":"19:36","pcpn":"0.0","pop":"4","pres":"1018","sr":"06:24","ss":"18:56","tmp_max":"28","tmp_min":"16","uv_index":"7","vis":"10","wind_deg":"97","wind_dir":"东风","wind_sc":"1-2","wind_spd":"9"},{"cond_code_d":"100","cond_code_n":"101","cond_txt_d":"晴","cond_txt_n":"多云","date":"2018-09-11","hum":"53","mr":"07:45","ms":"20:13","pcpn":"0.0","pop":"11","pres":"1016","sr":"06:25","ss":"18:55","tmp_max":"31","tmp_min":"16","uv_index":"4","vis":"20","wind_deg":"137","wind_dir":"东南风","wind_sc":"1-2","wind_spd":"2"},{"cond_code_d":"104","cond_code_n":"305","cond_txt_d":"阴","cond_txt_n":"小雨","date":"2018-09-12","hum":"51","mr":"08:50","ms":"20:49","pcpn":"0.0","pop":"4","pres":"1014","sr":"06:26","ss":"18:53","tmp_max":"28","tmp_min":"16","uv_index":"3","vis":"20","wind_deg":"124","wind_dir":"东南风","wind_sc":"1-2","wind_spd":"10"}]}]}'
    if data['HeWeather6'][0]['status'] == 'ok':
        now = data['HeWeather6'][0]['daily_forecast']
        val['next1_date'] = now[0]['date']
        val['next1_weather'] = now[0]['cond_code_d']
        val['next1_max'] = now[0]['tmp_max']
        val['next1_min'] = now[0]['tmp_min']
        val['next1_date'] = now[1]['date']
        val['next2_weather'] = now[1]['cond_code_d']
        val['next2_max'] = now[1]['tmp_max']
        val['next2_min'] = now[1]['tmp_min']
        val['next2_date'] = now[2]['date']
        val['next3_weather'] = now[2]['cond_code_d']
        val['next3_max'] = now[2]['tmp_max']
        val['next3_min'] = now[2]['tmp_min']
