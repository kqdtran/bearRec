import os
import pickle
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

def findSimilarity(model, term, num):
  """Find the similarity between the given term and 
  any of the vectors in the space"""

  doc = Document(term, stemmer=LEMMA, stopwords=True)
  return model.neighbors(doc, top=num)

def retrieveClassName():
  """Retrieve all the class names for autocomplete UI"""

  courseList = []
  for r, d, files in os.walk("project/data/"):
    for f in files:
      if f.endswith(".txt"):
        f = f.replace(".txt", "")
        courseList.append(f)
  pickle.dump(courseList, open("project/pickle/courseList.pic", "w"))

def loadClasses():
  classes = pickle.load(open("project/pickle/courseList.pic", "rb"))
  with open("project/pickle/courseList.txt", "w") as writer:
    for c in classes:
      writer.write("\"" + c + "\",\n")

if __name__ == "__main__":
  #runTFIDF()
  #model = loadTFIDF()
  #print findSimilarity(model, "algorithm", 10)
  #retrieveClassName()
  loadClasses()
