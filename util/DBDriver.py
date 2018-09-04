import sqlite3


# createtabsql1 = "create table if not exists scriptdata(id integer primary key autoincrement, name varchar(128), info varchar(128))"
from util.Config import Config


class DBDriver:
    '''
    The DBDriver class use to write the script data that parse from Excel file
    '''

    def __init__(self, tabledesc, dbfile=None):

        self.tablename = tabledesc[0]
        self.tablefield = tabledesc[1]
        if dbfile:
            self.dbfile = dbfile
        else:
            conf = Config()
            self.dbfile = str(conf.properties.get("ProjectRoot"))+str(conf.properties.get("DBFile"))
        self.conn = sqlite3.connect(self.dbfile)
        self.conn.isolation_level = None

    def cerateDB(self):
        createlist = ["create table if not exists ", self.tablename, "(",
                      self.tablefield, ")"]
        createsql = "".join(createlist)
        print(self.dbfile)

        # self.conn.execute("drop table if exists " + self.tablename)  ###delete the eixst table
        self.conn.execute(createsql)  ####create new table
        # conn.execute("delete from " + tablename) ####delete all the recoreds
        return

    def execDB(self, execsql,args=None):
        if args:
            self.conn.execute(execsql,args)
        else:
            self.conn.execute(execsql)
        self.conn.commit()
        return

    def getResult(self, selectsql,args=None):
        self.cur = self.conn.cursor()
        if args:
            self.cur.execute(selectsql,args)
        else:
            self.cur.execute(selectsql)

        self.res = self.cur.fetchall()
        self.cur.close()
        return self.res

    def getCount(self):
        return len(self.res)

    def closeDB(self):
        self.conn.close()
