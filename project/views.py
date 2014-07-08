from flask import request, render_template, jsonify
from flask.ext.classy import FlaskView
from app import app
import os
import util
from analyze import *


# Loads the model upfront from the pickle file
model = loadTFIDFModel(util.currentTerm, util.currentYear, True)


@app.route('/findSimilarCoursestoTerm', methods=['POST'])
def searchCourses():
    """
    """

    text, similarCourses = searchSimilar()
    jsonCourses = []
    for simCourse in similarCourses:
        course = simCourse[1].description
        jsonCourses.append(dict(
            course=course.UID.replace('.', ' '),
            title=course.title,
            location=course.location,
            time=course.time,
            instructor=course.instructor,
            description=course.description,
            score="{0:.2f}".format(simCourse[0])
        ))
    return jsonify(result=jsonCourses)


def searchSimilar():
    """
    """

    text = request.form.get('text')
    count = int(request.form.get('count'))
    similarCourses = findSimilarity(model, text, count)
    return text, similarCourses


class BaseView(FlaskView):
    """
    Basic views, such as the home and about page.
    """

    route_base = '/'

    def index(self):
        return render_template('home.html')


BaseView.register(app)
