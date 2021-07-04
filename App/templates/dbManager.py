import pymongo 

class DBManager:    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
    mydb = myclient["RistorantiDB"]
    ristoranti = mydb["ristoranti"]

    @staticmethod
    def search_byname(name):
        result = DBManager.ristoranti.find({"name":name})
        return result

if __name__=='__main__':
    result = DBManager.search_byname('#1 BUFFET')
    for x in result:
        print(x)
