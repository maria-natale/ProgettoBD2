from flask import Flask, request, render_template
from dbManager import DBManager

class SearchRestaurant:
    @staticmethod
    def search_restaurants(req):
        try:
            state = request.form['state_name']
        except KeyError:
            state = None
            city = request.form['city_name']
        city_flag = False
        if state:
            print(str(state))
            result = DBManager.search_bystate(str(state)) 
        else:
            result = DBManager.search_bycity(str(city))
            city_flag = True
        #ristoranti, città, cucina
        return render_template('visualize_restaurants.html', result = state, city_flag = city_flag, cuisine_flag = False )