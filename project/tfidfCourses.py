import os
import pickle
from pattern.vector import Document, Model, TFIDF, LEMMA
from scrapeCurrentSemester import loadAllCourses


def runTFIDF(term="SP", year=14):
  """Given a list of classes, construct a Vector-Space Model.
  We only need to do it once and save it to a pickle file for
  fast loading later on"""

  model = Model(documents=[], weight=TFIDF)
  allCourses = loadAllCourses()
  for course in allCourses:
    text = course.description
    doc = Document(text, stemmer=LEMMA, stopwords=True, name=course.name,\
                   description=course) # save the course for frontend use later
    model.append(doc)
  model.save("pickle/simCourses" + term + str(year) + ".pickle")

def loadTFIDF(term="SP", year=14):
  """Load the pickle file created by runTFIDF"""

  return Model.load("pickle/simCourses" + term + str(year) + ".pickle")

def findSimilarity(model, term, num):
  """Find the similarity between the given term and 
  any of the vectors in the space"""

  doc = Document(term, stemmer=LEMMA, stopwords=True)
  return model.neighbors(doc, top=num)

if __name__ == "__main__":
  #runTFIDF()
  model = loadTFIDF()
  print findSimilarity(model, "algorithms", 10)
