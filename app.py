#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020  <@176a5ba06ba6>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Flask, escape, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/index')
def hello():
	return 'Welcome to test my page'

@app.route('/user/<user>')
def user(user):
	return 'User is %s' % escape(user)

@app.route('/test')
def test1():
	print(url_for('hello'))
	print(url_for('user', user='wmsj100'))
	print(url_for('test1'))
	return 'Test page'

if __name__ == '__main__':
	app.run(debug=True,port=80, host='0.0.0.0')
