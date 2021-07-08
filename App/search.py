from flask import Flask, request, render_template, session
from flask_paginate import Pagination, get_page_args
from dbManager import DBManager
import random

class SearchRestaurant:
    ROWS_PER_PAGE = 10

    @staticmethod
    def get_restaurants(restaurants, offset=0, per_page=10):
        return restaurants[offset: offset + per_page]

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
        

        try:
            city_flag = False if session['city_flag'] is None else session['city_flag']
        except KeyError:
            city_flag = False
        try:
            cuisine_flag = False if session['cuisine_flag'] is None else session['cuisine_flag']
        except KeyError:
            cuisine_flag = False
        print(state)

        if state:
            print(str(state))
            if state == 'New York' or state == 'Illinois':
                cuisine_flag = True
            #result = DBManager.search_bystate(str(state)) 
        else:
            #result = DBManager.search_bycity(str(city))
            city_flag = True
        risks = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'Not Yet Graded']

        res_type = None
        try:
            ordine = request.form['ordina_rischio']
        except KeyError:
            try:
                ordine = session['ordine']
            except KeyError:
                ordine = 1

        result = DBManager.filter_restaurants(state = state, city = city, risks= risks, res_type = res_type, risk_order=ordine)

        session['risks'] = risks
        session['res_type'] =  False
        session['ordine'] = 1
        session['city_flag'] = city_flag
        
        if len(result)>0:
            state = result[0]['state']
        if state == 'New York' or state == 'Illinois':
                cuisine_flag = True
        
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
                           pagination=pagination, state = state, city_flag = city_flag, 
                            cuisine_flag = cuisine_flag, risks = risks, ordine = 1
                           )
    

    @staticmethod
    def filter_restaurant(req):
        risks = request.form.getlist('check')
        if len(risks)==0:
            risks = session['risks']

        try:
            city = request.form['city_name']
        except KeyError:
            city = session['city']
        if city == '':
            city = None

        try:
            res_type = request.form['res_type']
        except KeyError:
            try:
                res_type = session['res_type']
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
    
        result = DBManager.filter_restaurants(state = state, city = city, risks= risks, res_type = res_type, risk_order=ordine)
        session['risks'] = risks
        session['res_type'] =  None
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
        print(risks)
        pagination_res = SearchRestaurant.get_restaurants(result, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
        return render_template('visualize_restaurants.html',
                           restaurants=pagination_res,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, risks = risks, state = state,
            res_type = res_type, ordine = ordine, city_flag = city_flag, cuisine_flag = cuisine_flag)
    

    @staticmethod
    def search_by_type(req):
        cavia=request.form['type']
        result=DBManager.searchrestype(str(cavia))
        return render_template('visualize_restaurants.html', value = result)


    @staticmethod
    def search_restaurants_type(req):
        risks = ['Risk 1 (High)', 'Risk 2 (Medium)', 'Risk 3 (Low)', 'Not Yet Graded']
        args =request.args
        cavia = args["valore"]
        print(str(cavia))
        result = DBManager.search_bytype(str(cavia))

        page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
        print(page, per_page, offset)
        total = len(result)
        print(total)
        pagination_res = SearchRestaurant.get_restaurants(result, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
            
        session['res_type'] = str(cavia)
        session['state'] = 'New York'
        session['city_flag'] = False
        session['cuisine_flag'] = False
        print(pagination_res)
        return render_template('visualize_restaurants.html',
                           restaurants=pagination_res,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, risks = risks, state = 'New York',
            res_type = str(cavia), ordine = 1, city_flag = False, cuisine_flag = False)
    
    
    @staticmethod
    def rischiare(req):
        result = DBManager.search_byrisk()
        x=random.sample(range(0,result.count()),8)
        cavia=[]
        for i in x:
            cavia.append(result[i])
            print(cavia)

        return cavia
    

    @staticmethod
    def search_type(req):
        result = DBManager.searchtype()
        x=random.sample(range(0,len(result)),12)
        cavia=[]
        print(x)

        for i in x:
            if i==12 or i==69 or i==50 or i ==48 or i==40 or i==10:
                cavia.append(result[i+1])
            else:
                cavia.append(result[i])
        return cavia

    @staticmethod
    def tutte(req):

        result = DBManager.searchtype()
        return result
    

    @staticmethod
    def search_by_type(req):
        cavia=request.form['type']
        result=DBManager.searchrestype(str(cavia))
        return render_template('visualize_restaurants.html', value = result)