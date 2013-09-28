from flask import render_template  # ...etc , redirect, request, url_for
from flask.ext.classy import FlaskView
from app import app

class BaseView(FlaskView):
  '''Basic views, such as the home and about page.'''
  route_base = '/'

  def index(self):
    return render_template('home.html')

BaseView.register(app)
