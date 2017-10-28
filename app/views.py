#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 13:19:08 2017

@author: beaubritain
"""
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/results')
def results():
    return render_template('results.html',
                           title='Results', 
                           estimated_fare=12.34, 
                           estimated_tip=4.20)    

# remove this when we deploy on apache, and route the static content separately
@app.route('/static/<path:path>')
def static_content(path):
    return send_from_directory('static', path)
