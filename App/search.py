from flask import Flask, request, render_template, session
from flask_paginate import Pagination, get_page_args
from dbManager import DBManager
from bson import ObjectId


class SearchRestaurant:
    ROWS_PER_PAGE = 10

    db = None

    @staticmethod
    def get_restaurants(restaurants, offset=0, per_page=10):
        return restaurants[offset: offset + per_page]

    @staticmethod
    def get_information(id):
        db = DBManager()
        db.connect()
        objInstance = ObjectId(id)
        result = db.db.find_one({"_id": objInstance})
        ordine = -1
        txt = result['violations']
        finalArray = []

        for var in txt:
            lenght = len(var)
            if lenght == 3:
                x = var['description'].replace("        points  ...   violation_status", "")
                x = x[:-20]
                points = x.replace("  ...  OUT OF COMPLIANCE", "")
                arreyPoints = points.splitlines()
                arreyPoints = arreyPoints[1:-1]
                arrayData = {"violazione" : var['inspection_date'].date(), "descrizione" : arreyPoints, "rischio" : var['risk'], "descrizioneSingola" : var['description']}
                finalArray.append(arrayData)
            else:
                arrayData = {"violazione" : var['inspection_date'].date(), "descrizione" : 'Nessuna descrizione', "rischio" : var['risk'], "descrizioneSingola" : 'Nessuna descrizione'}
                finalArray.append(arrayData)
        #print(result)
        #print(finalArray)
        return render_template('detail_restaurant.html',
                               restaurants=result, points=finalArray, ordine=ordine)

    @staticmethod
    def search_restaurants(req):
        try:
            state = request.form['state_name']
        except KeyError:
            state = session['state']

        try:
            city = request.form['city_name']
        except KeyError:
            try:
                city = session['city']
            except KeyError:
                city = None

        city_flag = False if session['city_flag'] is None else session['city_flag']
        cuisine_flag = False if session['cuisine_flag'] is None else session['cuisine_flag']
        print(state)

        if state:
            print(str(state))
            if state == 'New York' or state == 'Illinois':
                cuisine_flag = True
            # result = DBManager.search_bystate(str(state))
        else:
            # result = DBManager.search_bycity(str(city))
            city_flag = True
        risks = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'Not Yet Graded']

        res_type = None
        try:
            ordine = request.form['ordina_rischio']
        except KeyError:
            ordine = session['ordine']

        result = DBManager.filter_restaurants(state=state, city=city, risks=risks, res_type=res_type, risk_order=ordine)

        session['risks'] = risks
        session['res_type'] = False
        session['ordine'] = 1
        session['city_flag'] = city_flag
        session['cuisine_flag'] = cuisine_flag
        session['state'] = state
        session['city'] = city

        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')

        total = len(result)
        print(total)
        pagination_res = SearchRestaurant.get_restaurants(result, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('visualize_restaurants.html',
                               restaurants=pagination_res,
                               page=page,
                               per_page=per_page,
                               pagination=pagination, state=state, city_flag=city_flag,
                               cuisine_flag=cuisine_flag, risks=risks, ordine=1
                               )

    @staticmethod
    def filter_restaurant(req):
        risks = request.form.getlist('check')
        print(risks)

        try:
            city = request.form['city_name']
        except KeyError:
            city = session['city']
        if city == '':
            city = None

        try:
            res_type = request.form['res_type']
        except KeyError:
            res_type = None
        if res_type == '':
            res_type = None

        try:
            ordine = request.form['ordina_rischio']
        except KeyError:
            ordine = session['ordine']

        state = session['state']
        cuisine_flag = False
        if state:
            print(str(state))
            if state == 'New York' or state == 'Illinois':
                cuisine_flag = True
        if city is None:
            city_flag = False
        else:
            city_flag = True

        result = DBManager.filter_restaurants(state=state, city=city, risks=risks, res_type=res_type, risk_order=ordine)
        session['risks'] = risks
        session['res_type'] = None
        session['ordine'] = int(ordine)
        session['city_flag'] = city_flag
        session['cuisine_flag'] = cuisine_flag
        session['state'] = state
        session['city'] = city

        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        print(page, per_page, offset)
        total = len(result)
        print(total)
        pagination_res = SearchRestaurant.get_restaurants(result, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        return render_template('visualize_restaurants.html',
                               restaurants=pagination_res,
                               page=page,
                               per_page=per_page,
                               pagination=pagination, risks=risks, state=state,
                               res_type=res_type, ordine=ordine, city_flag=city_flag, cuisine_flag=cuisine_flag)

    @staticmethod
    def filter_violations(req):
        idRestaurant = request.form['id']

        try:
            ordine = request.form['ordina_data']
        except KeyError:
            ordine = -1

        result = DBManager.filter_violations(id=idRestaurant, date_order=int(ordine))
        print(idRestaurant)
        print(result)
        result = result[0]
        txt = result['violations']
        finalArray = []

        for var in txt:
            lenght = len(var)
            if lenght == 3:
                x = var['description'].replace("        points  ...   violation_status", "")
                x = x[:-20]
                points = x.replace("  ...  OUT OF COMPLIANCE", "")
                arreyPoints = points.splitlines()
                arreyPoints = arreyPoints[1:-1]
                arrayData = {"violazione": var['inspection_date'].date(), "descrizione": arreyPoints,
                             "rischio": var['risk'], "descrizioneSingola": var['description']}
                finalArray.append(arrayData)
            else:
                arrayData = {"violazione": var['inspection_date'].date(), "descrizione": 'Nessuna descrizione',
                             "rischio": var['risk'], "descrizioneSingola": 'Nessuna descrizione'}
                finalArray.append(arrayData)

        return render_template('detail_restaurant.html',
                               restaurants=result, points=finalArray, ordine=int(ordine))
