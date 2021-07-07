import os

from flask import Flask, render_template, request, session
from search import SearchRestaurant
from dbManager import DBManager
from flask_paginate import get_page_args


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def welcome():
        session['city'] = None
        session['state'] = None
        session['city_flag'] = None
        session['risks'] = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'Not Yet Graded']
        session['res_type'] =  None
        session['ordine'] = 1
        session['cuisine_flag'] = None
        return render_template('index.html')
    
    @app.route('/search_restaurant', methods=['POST', 'GET'])
    def handle_data():
        return SearchRestaurant.search_restaurants(request)
    

    @app.route('/filter_restaurants', methods=['POST', 'GET'])
    def filter():
        return SearchRestaurant.filter_restaurant(request)

    @app.route('/get_information', methods=['POST', 'GET'])
    def getRestaurant():
        id = request.form['id']
        print(f'Id ristorante: {id}')
        return SearchRestaurant.get_information(id)
        #return render_template('detail_restaurant.html')
    

    return app



if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)