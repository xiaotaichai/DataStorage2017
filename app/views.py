#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 13:19:08 2017

@author: beaubritain
"""
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import DataRequired
from app import app, queries

sql_engine = queries.get_engine()

class LocationForm(FlaskForm):
    from_lat = DecimalField('from_lat', places=4, validators=[DataRequired()], render_kw={"placeholder": "Latitude", "class": "form-control"})
    from_long = DecimalField('from_long', places=4, validators=[DataRequired()], render_kw={"placeholder": "Longitude", "class": "form-control"})
    to_lat = DecimalField('to_lat', places=4, validators=[DataRequired()], render_kw={"placeholder": "Latitude", "class": "form-control"})
    to_long = DecimalField('to_long', places=4, validators=[DataRequired()], render_kw={"placeholder": "Longitude", "class": "form-control"})

@app.route('/')
@app.route('/index')
def index():
    form = LocationForm(csrf=False)
    return render_template('index.html',
                           title='Home', form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
    form = LocationForm(csrf=False)
    if not form.validate_on_submit():
        # maybe flash a message
        return redirect('/')
    sql_connection = sql_engine.connect()
    result = sql_connection.execute(queries.generate_comparables_query(form.from_lat.data, 
                                                                       form.from_long.data, 
                                                                       form.to_lat.data, 
                                                                       form.to_long.data))
    estimated_fare, estimated_tip = result.fetchone()
    result.close()
    return render_template('results.html',
                           title='Results', 
                           estimated_fare=estimated_fare, 
                           estimated_tip=estimated_tip)    

# remove this when we deploy on apache, and route the static content separately
@app.route('/static/<path:path>')
def static_content(path):
    return send_from_directory('static', path)
