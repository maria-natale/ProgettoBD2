import pymongo 
from flask import Flask,render_template,request,make_response,jsonify
from bson.json_util import dumps
from pprint import pprint
class DBManager:
    db = None

    def connect(self):
        client = pymongo.MongoClient("localhost:27017")
        db = client['RistorantiDB']
        self.db=db['ristoranti']
        

    def query(self, sql):
      cursor = self.conn.find(sql)  
      return cursor 
 

    @staticmethod
    def search_bycity(name):
        db = DBManager()
        db.connect()
        result = db.db.find({"name":name})
        return list(result)
    
    @staticmethod
    def search_bystate(state):
        db = DBManager()
        db.connect()
        print(state)
        result = db.db.find({"state":state})
        print(result)
        return list(result)
    

    @staticmethod
    def filter_restaurants(state = None, city = None, 
        risks = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'Not Yet Graded'], res_type = None, risk_order = -1):
        db = DBManager()
        db.connect()
        myMatch = {}

        if state is not None:
            myMatch['state'] = state
            if state == 'New York' and res_type is not None:
                myMatch['cuisine_description'] = res_type
            elif state == 'Illinois' and res_type is not None:
                myMatch['type'] = res_type
        if city is not None:
            myMatch['city'] = city
        print(myMatch)
        result = db.db.aggregate([
            {"$match" : myMatch},
            { "$project" : {
                "_id" : 0,
                "name":1,
                "address":1,
                "city" : 1,
                "zipcode": 1,
                "state":1,
                "rischia": { "$first": "$violations.risk" },
                "order" : {
                    "$cond" : {
                        "if" : { "$eq" : ["$rischia" , "Risk 3 (Low)"] }, "then" : 1,
                        "else"  : { "$cond" : {
                        "if" : { "$eq" : ["$rischia", "Risk 2 (Medium)"] }, "then" : 2, 
                            "else"  : 3
                        }
                    }
                    }
                },
            "has_risk": {"$in": [{"$first": "$violations.risk"}, ['Risk 1 (High)']]}
            } }, 
            {"$sort" : {"order" : int(risk_order)} }
        ])
        
        result = list(result)
        new = []
        for x in result:
            if x['has_risk']:
                new.append(x)

        return new



if __name__=='__main__':
    result = DBManager.filter_restaurants(state = 'New York', risk_order=1)
    for x in result[:2]:
        print(x)

