import util.UserDao as UserDao
import util.Config as Config
import os
def install():
    print("Install DB")
    installDB()



def installDB():
    try:
        config = Config.Config()
        dbFileSrc = config.properties.get("ProjectRoot")+config.properties.get("DBFile")
        if os.path.exists(dbFileSrc):
            print("remove DB")
            os.remove(dbFileSrc)
        else:
            print("create DB")
            os.system("sqlite3 "+str(config.properties.get("ProjectRoot")+config.properties.get("DBFile"))+" .exit")

            print("Init table")
            UserDao.initDB()
    except Exception as e:
        raise e