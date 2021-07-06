import os

from flask import Flask, render_template, request
from search import SearchRestaurant



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

    # a simple page that says hello
    @app.route('/')
    def welcome():
        return render_template('index.html')
    
    @app.route('/search_restaurant', methods=['POST'])
    def handle_data():
        state = request.form['state_name']
        app.logger.info(f"Stato: {state}")
        return SearchRestaurant.search_restaurants(request)

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)