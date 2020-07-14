#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020  <@176a5ba06ba6>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Flask, escape, url_for, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/index')
def hello():
	name = 'Grey Li'
	movies = [
			{'title': 'My Neighbor Totoro', 'year': '1988'},
			{'title': 'Dead Poets Society', 'year': '1989'},
			{'title': 'A Perfect World', 'year': '1993'},
			{'title': 'Leon', 'year': '1994'},
			{'title': 'Mahjong', 'year': '1996'},
			{'title': 'Swallowtail Butterfly', 'year': '1996'},
			{'title': 'King of Comedy', 'year': '1999'},
			{'title': 'Devils on the Doorstep', 'year': '1999'},
			{'title': 'WALL-E', 'year': '2008'},
			{'title': 'The Pork of Music', 'year': '2012'},
			]

	return render_template('index.html', name=name, movies=movies)

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
