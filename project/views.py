from flask import render_template  # ...etc , redirect, request, url_for
from flask.ext.classy import FlaskView
from app import app
import os
from pattern.vector import Document, Model, TFIDF, LEMMA
from tfidf import *

@app.route('/findSimilarCoursestoTerm', methods=['POST'])
def search_similar():
	text = request.form.get('text')
	findSimilarity(model, text)

class BaseView(FlaskView):
  	'''Basic views, such as the home and about page.'''
  	route_base = '/'

	def index(self):
		model = loadTFIDF()
		return render_template('home.html')

BaseView.register(app)
