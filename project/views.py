from flask import request, render_template, jsonify
from flask.ext.classy import FlaskView
from app import app
import os
from tfidfCourses import *
#import networkx as nx
#import matplotlib.pyplot as plt


model = loadTFIDFModel("Spring", "2014", True)

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
  text = request.form.get('text')
  count = int(request.form.get('count'))
  similarCourses = findSimilarity(model, text, count)
  return text, similarCourses

class BaseView(FlaskView):
  '''Basic views, such as the home and about page.'''
  route_base = '/'

  def index(self):
    return render_template('home.html')

BaseView.register(app)
