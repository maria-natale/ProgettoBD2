import pymongo 
from flask import Flask,render_template,request,make_response,jsonify
from bson.json_util import dumps
from pprint import pprint
class DBManager:
    db = None

    def connect(self):
        client = pymongo.MongoClient("localhost:27017")
        db = client.Ristoranti
        self.db=db.ristoranti
        

    def query(self, sql):
      cursor = self.conn.find(sql)  
      return cursor 
 
    #serverStatusResult=mydb.command("serverStatus")
    #pprint(serverStatusResult)



    @staticmethod
    def search_byname(name):
        result = DBManager.ristoranti.find({"name":name})
        return result
    
    @staticmethod
    def search_bystate(state):
        db = DBManager()
        db.connect()
        print(state)
        result = db.db.find({"state":state})
        print("culo nudo")
        print(result)
        return result

if __name__=='__main__':
    result = DBManager.search_byname('#1 BUFFET')
    print(dumps(result))
    #for x in result:
     #   print(x)
