from flask import Flask, request, render_template
from dbManager import DBManager

class SearchRestaurant:
    @staticmethod
    def search_restaurants(req):
        state = request.form['state_name']
        print(str(state))
        result = DBManager.search_bystate(str(state))
        return render_template('visualize_restaurants.html', value = state)