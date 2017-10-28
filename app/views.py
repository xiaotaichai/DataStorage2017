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
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/results')
def results():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('results.html',
                           title='Home',
                           user=user)    


