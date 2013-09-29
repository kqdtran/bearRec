from flask import request, render_template, jsonify  # ...etc , redirect, request, url_for
from flask.ext.classy import FlaskView
from app import app
import os
from pattern.vector import Document, Model, TFIDF, LEMMA
from tfidf import *
import networkx as nx
import matplotlib.pyplot as plt

model = loadTFIDF()

@app.route('/findSimilarCoursestoTerm', methods=['POST'])
def searchCourses():
  text, similarCourses = searchSimilar()
  #graphSimilar(text, similarCourses)
  jsonCourses = [dict(course = c[1].name, 
    score = "{0:.2f}".format(c[0])) for c in similarCourses]
  return jsonify(result = jsonCourses)

def graphSimilar(text, similarCourses):
  graph = nx.Graph()
  for c in similarCourses:
    graph.add_edge(text, c[1].name, weight=c[0])
  nx.draw(graph)
  plt.savefig("path.png")

def searchSimilar():
  numSearch = 10 # WE CAN CHANGE THIS LATER TO LET THE USER DETERMINES HOW MANY RESULTS
  text = request.form.get('text')
  similarCourses = findSimilarity(model, text, numSearch)
  return text, similarCourses

class BaseView(FlaskView):
  '''Basic views, such as the home and about page.'''
  route_base = '/'

  def index(self):
    return render_template('home.html')

BaseView.register(app)
