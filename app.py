#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020  <@176a5ba06ba6>
# https://read.helloflask.com/c6-template2#zi-ding-yi-cuo-wu-ye-mian
# Distributed under terms of the MIT license.

"""

"""
from flask import Flask, escape, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))

class Movies(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	year = db.Column(db.String(4))

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
	if drop:
		click.echo('Drop all data')
		db.drop_all()
	db.create_all()
	click.echo('Initialized database.')

@app.cli.command()
def forge():
	db.create_all()
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
	user = User(name=name)
	db.session.add(user)

	for m in movies:
		movie = Movies(title=m['title'], year=m['year'])
		db.session.add(movie)
	
	db.session.commit()
	click.echo('Install template data OK!')

@app.route('/')
@app.route('/home')
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		title = request.form.get('title')
		year = request.form.get('year')

		if not title or not year or len(year) != 4 or len(title) > 60:
			flash('Invalid input')
			return redirect(url_for('index'))
		movie = Movies(title=title, year=year)
		db.session.add(movie)
		db.session.commit()
		flash('Item {} Created'.format(title))
		return redirect(url_for('index'))
	elif request.method == 'GET':
		movies = Movies.query.all()

	return render_template('index.html', movies=movies)
@app.route('/user/<user>')
def user(user):
	return 'User is %s' % escape(user)


@app.context_processor
def inject_user():
	user = User.query.first()
	return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/test')
def test1():
	print(url_for('index'))
	print(url_for('user', user='wmsj100'))
	print(url_for('test1'))
	return 'Test page'

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
	movie = Movies.query.get_or_404(movie_id)

	if request.method == 'POST':
		title = request.form['title']
		year = request.form['year']

		if not title or not year or len(year) != 4 or len(title) > 60:
			flash('Invalid input')
			return redirect(url_for('edit', movie_id=movie_id))

		movie.title = title
		movie.year = year
		db.session.commit()
		flash('Item update')
		return redirect(url_for('index'))
	return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
	movie = Movies.query.get_or_404(movie_id)
	db.session.delete(movie)
	db.session.commit()
	flash('Delete Item OK')
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True,port=80, host='0.0.0.0')
