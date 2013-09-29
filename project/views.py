from flask import request, render_template, jsonify  # ...etc , redirect, request, url_for
from flask.ext.classy import FlaskView
from app import app
import os
from pattern.vector import Document, Model, TFIDF, LEMMA
from tfidf import *

@app.route('/findSimilarCoursestoTerm', methods=['POST'])
def search_similar():
  model = loadTFIDF()
  text = request.form.get('text')
  similarCourses = findSimilarity(model, text)
  jsonCourses = [dict(course = c[1].name, score = c[0]) for c in similarCourses]
  return jsonify(result = jsonCourses)

class BaseView(FlaskView):
  '''Basic views, such as the home and about page.'''
  route_base = '/'

  def index(self):
    model = loadTFIDF()
    return render_template('home.html')

BaseView.register(app)
