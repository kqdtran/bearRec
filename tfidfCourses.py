import os
import pickle
from pattern.vector import Document, Model, TFIDF, LEMMA
from scrapeBerkeleyAPI import loadCourseCatalog, loadAllCoursesInTerm
from pprint import pprint


def runTFIDFOnCatalog(term="Spring", year="2014"):
  """
  Given a dictionary of courses, construct a Vector-Space model 
  and apply the TFIDF algorithm to measure similarity between courses.
  
  We only need to do it once and save it to a pickle file for
  fast loading later on
  """
  model = Model(documents=[], weight=TFIDF)
  print "Loading from pickle file..."
  #allCoursesDict = loadCourseCatalog()

  for dept in allCoursesDict:
    print "Processing department", dept
    for course in allCoursesDict[dept]:
      text = course.title + " " + course.description
      doc = Document(text, stemmer=LEMMA, stopwords=True, name=course.title,\
                     description=course)
      model.append(doc)
    print "Finish processing", dept, "\n"
  model.save("pickle/simCatalog" + term + year + ".pickle")

def runTFIDFOnSchedule(term="Spring", year="2014"):
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
  model.save("pickle/simCourses" + term + year + ".pickle")

def loadTFIDFModel(term="Spring", year="2014", schedule=True):
  """
  Load the pickle file created by runTFIDF
  """
  if schedule:
    return Model.load("pickle/simCourses" + term + year + ".pickle")
  else:  # load from catalog instead
    return Model.load("pickle/simCatalog" + term + year + ".pickle")

def findSimilarity(model, term, num):
  """
  Find the similarity between the given term and 
  all of the vectors in the space, and output the 
  best "num" result in descending
  """
  doc = Document(term, stemmer=LEMMA, stopwords=True)
  return model.neighbors(doc, top=num)

if __name__ == "__main__":
  # ---- On catalog ----
  #runTFIDFOnCatalog()
  #model = loadTFIDF("Spring", "2014", False)
  #print findSimilarity(model, "algorithms", 10)

  # ---- On schedule of classes ----
  #runTFIDFOnSchedule()
  model = loadTFIDFModel("Spring", "2014", True)
  print findSimilarity(model, "algorithms", 10)
