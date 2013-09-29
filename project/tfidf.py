import os
from pattern.vector import Document, Model, TFIDF, LEMMA

def readFile(filename):
  """Read a text file with the given file name and return
  its content"""

  with open("project/data/" + filename, "r") as f:
    return " ".join(f.readlines()).strip()

def runTFIDF():
  """Given a list of classes, construct a Vector-Space Model.
  We only need to do it once and save it to a pickle file for
  fast loading later on"""

  model = Model(documents=[], weight=TFIDF)
  for r, d, files in os.walk("project/data/"):
    for f in files:
      if f.endswith(".txt"):
        text = readFile(f)
        doc = Document(text, stemmer=LEMMA, stopwords=True, name=f.replace(".txt", ""))
        model.append(doc)
  model.save("project/pickle/course.pic")

def loadTFIDF():
  """Load the pickle file created by run TFIDF"""

  return Model.load("project/pickle/course.pic")

def findSimilarity(model, term):
  """Find the similarity between the given term and 
  any of the vectors in the space"""

  doc = Document(term)
  return model.neighbors(doc)

class SimilarCourse(object):
  def __init__(self, course, score):
    self.course = course
    self.score = score

if __name__ == "__main__":
  #runTFIDF()
  model = loadTFIDF()
  print findSimilarity(model, "algorithm")
