#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 13:19:08 2017

@author: beaubritain
"""
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import DataRequired
from app import app, queries

sql_engine = queries.get_engine()

create_render_kw = lambda coordinate: {"placeholder": coordinate, "class": "form-control", "type": "number", "step": "any"}

class LocationForm(FlaskForm):
    from_lat = DecimalField('Origin Latitude', places=4, validators=[DataRequired()], render_kw=create_render_kw("Latitude"))
    from_long = DecimalField('Origin Longitude', places=4, validators=[DataRequired()], render_kw=create_render_kw("Longitude"))
    to_lat = DecimalField('Destination Latitude', places=4, validators=[DataRequired()], render_kw=create_render_kw("Latitude"))
    to_long = DecimalField('Destination Longitude', places=4, validators=[DataRequired()], render_kw=create_render_kw("Longitude"))

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
        for field in form:
          if not field.validate(form):
            flash("Invalid value for {name}".format(name=field.label.text))
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
                           estimated_tip=estimated_tip, 
                           origin="{0},{1}".format(form.from_lat.data, form.from_long.data),
                           destination="{0},{1}".format(form.to_lat.data, form.to_long.data))    

# remove this when we deploy on apache, and route the static content separately
@app.route('/static/<path:path>')
def static_content(path):
    return send_from_directory('static', path)
