import os
import util
from pattern.vector import Document, Model, TFIDF, LEMMA
from scrapeBerkeleyAPI import loadCourseCatalog, loadAllCoursesInTerm
from pprint import pprint
from cPickle import load, dump


def runTFIDFOnCatalog(term=util.currentTerm, year=util.currentYear):
  """
  Given a dictionary of courses, construct a Vector-Space model 
  and apply the TFIDF algorithm to measure similarity between courses.
  
  We only need to do it once and save it to a pickle file for
  fast loading later on
  """

  model = Model(documents=[], weight=TFIDF)
  print "Loading from pickle file..."
  allCoursesDict = loadCourseCatalog()

  for dept in allCoursesDict:
    print "Processing department", dept
    for course in allCoursesDict[dept]:
      text = course.title + " " + course.description
      doc = Document(text, stemmer=LEMMA, stopwords=True, name=course.title,\
                     description=course)
      model.append(doc)
    print "Finish processing", dept, "\n"
  with open("pickle/simCatalog" + term + year + ".pickle", "w") as f:
    dump(model, f, 0)
  return model


def runTFIDFOnSchedule(term=util.currentTerm, year=util.currentYear):
  """
  Given a list of classes, construct a Vector-Space model
  and apply the TFIDF algorithm to measure similarity between courses
  """

  model = Model(documents=[], weight=TFIDF)
  print "Loading from pickle file..."
  allCourses = loadAllCoursesInTerm()
  print "Begin constructing the Vector Space model"

  for course in allCourses:
    text = course.title + " " + course.description
    doc = Document(text, stemmer=LEMMA, stopwords=True, name=course.title,\
                   description=course)
    model.append(doc)
  print "Finish processing!!!"
  with open("pickle/simCourses" + term + year + ".pickle", "w") as f:
    dump(model, f, 0)
  return model


def loadTFIDFModel(term=util.currentTerm, year=util.currentYear, schedule=True):
  """
  Load the pickle file created by runTFIDF
  """

  if schedule:
    filename = "pickle/simCourses" + term + year + ".pickle"
    if os.path.exists(filename):
      with open(filename, "r") as f:
        return load(f)
    else:
      return runTFIDFOnSchedule(term, year)

  else:   # load from catalog instead
    filename = "pickle/simCatalog" + term + year + ".pickle"
    if os.path.exists(filename):
      with open(filename, "r") as f:
        return load(f)
    else:
      return runTFIDFOnCatalog(term, year)


def findSimilarity(model, inputTerm, num):
  """
  Find the similarity between the given term and 
  all of the vectors in the space, and output the 
  best "num" result in descending
  """

  doc = Document(inputTerm, stemmer=LEMMA, stopwords=True)
  return model.neighbors(doc, top=num)


if __name__ == "__main__":
  model = loadTFIDFModel(util.currentTerm, util.currentYear, True)
  print findSimilarity(model, "algorithms", 10)
