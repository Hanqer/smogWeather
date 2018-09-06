import pymysql

class sqlFactory:
    def __init__(self, user, pwd, dbName):
        self.db = pymysql.connect("localhost", user, pwd, dbName)
        self.cursor = self.db.cursor()

    def dropTable(self, tableName):
        sql = 'drop table if exists %s' % (tableName)
        self.cursor.execute(sql)
        self.db.commit()
    
    def initTable(self):
        sql = """CREATE TABLE IF NOT EXISTS WEATHER(
                CITY VARCHAR(20) NOT NULL PRIMARY KEY,
                SK_TEMP VARCHAR(10),
                SK_WIND_DIRECTION VARCHAR(10),
                SK_WIND_STRENGTH VARCHAR(10),
                SK_HUMIDITY VARCHAR(10),
                TODAY_TEMP VARCHAR(20),
                TODAY_WEATHER VARCHAR(20),
                DRESSING_ADVICE VARCHAR(100),
                UV_INDEX VARCHAR(10)
                ) """  
        self.cursor.execute(sql)
        self.db.commit()

    def insertData(self, val):
        sql = """REPLACE INTO weather(CITY, SK_TEMP, SK_WIND_DIRECTION, SK_WIND_STRENGTH, SK_HUMIDITY, TODAY_TEMP, TODAY_WEATHER, DRESSING_ADVICE, UV_INDEX) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """ % (val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8])
        #print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        self.db.close()