import pymongo 
from flask import Flask,render_template,request,make_response,jsonify
from bson.json_util import dumps
from pprint import pprint
import random
from bson import ObjectId

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
    def search_byid(id):
        db = DBManager()
        db.connect()
        result = db.db.find({"_id": id})
        return list(result)

    

    @staticmethod
    def filter_restaurants(state = None, city = None, 
        risks = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'Not Yet Graded'], res_type = None, risk_order = 1, skip = 0, limit = 10):
        db = DBManager()
        db.connect()
        myMatch = {}

        if state is not None:
            myMatch['state'] = state
            if state == 'New York' and res_type is not None:
                myMatch['cuisine_description'] = res_type
            elif state == 'Illinois' and res_type is not None:
                myMatch['restaurant_type'] = res_type.lower()
        if city is not None:
            myMatch['city'] = city.lower()
        print(myMatch)
        result = db.db.aggregate([
            {
                "$match": myMatch
            },
            {
                "$project": {
                "_id": 1,
                "name": 1,
                "address": 1,
                "city": 1,
                "zipcode": 1,
                "cuisine_description":1,
                "restaurant_type": 1,
                "state": 1,
                "rischia": {
                    "$first": "$violations.risk"
                },
                "order": {
                    "$cond": {
                    "if": {
                        "$eq": [
                        {
                            "$first": "$violations.risk"
                        },
                        "Risk 3 (Low)"
                        ]
                    },
                    "then": 1,
                    "else": {
                        "$cond": {
                        "if": {
                            "$eq": [
                            {
                                "$first": "$violations.risk"
                            },
                            "Risk 2 (Medium)"
                            ]
                        },
                        "then": 2,
                        "else": 3
                        }
                    }
                    }
                },
                "has_risk": {"$in": [{"$first": "$violations.risk"}, risks]}
                }
            },
            {
                "$sort": {
                "order": int(risk_order)
                }
            }
            ])
        
        
        result = list(result)
        new = []
        for x in result:
            if x['has_risk']:
                new.append(x)

        return new


    @staticmethod
    def searchrestype(cavia):
        db = DBManager()
        db.connect()
        result=db.db.find({"cuisine_description": cavia})
        return list(result)
    
    
    @staticmethod
    def search_bytype(typo):
        db = DBManager()
        db.connect()
        result=db.db.find({"cuisine_description":typo})
        return list(result)
    
    
    @staticmethod
    def searchtype():
        db = DBManager()
        db.connect()
        result = db.db.distinct("cuisine_description")
        return result
    

    @staticmethod
    def search_byrisk():
        db = DBManager()
        db.connect()
        result = db.db.find({"violations.0.risk": "Risk 3 (Low)"},{"name":1,"_id":1})
      
        return result


    


    @staticmethod
    def tutte(req):
        result = DBManager.searchtype()
        return result


    @staticmethod
    def search_type(req):
        print("culo")
        result = DBManager.searchtype()
        x=random.sample(range(0,len(result)),12)
        cavia=[]

        for i in x:
            if i==12 or i==69 or i==50 or i ==48 or i==40 or i==10:
                cavia.append(result[i+1])
            else:
                cavia.append(result[i])
        return cavia

    
    @staticmethod
    def filter_violations(id = None, date_order=-1):
        db = DBManager()
        db.connect()

        result = db.db.aggregate([
                {
                    "$match": {
                        "_id": ObjectId(id)
                    }
                },
                { "$unwind": '$violations' },
                {
                    "$sort": {
                        "violations.inspection_date": date_order
                    }
                }
        ])

        print(date_order)
        return list(result)


if __name__=='__main__':
    result = DBManager.filter_restaurants(state = 'New York', risk_order=1)
    for x in result[:2]:
        print(x)

