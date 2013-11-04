import requests
from bs4 import BeautifulSoup
from cPickle import load, dump

class Course():
  def __init__(self, name, courseTitle, location, instructor, ccn, note, description):
    self.name = name
    self.courseTitle = courseTitle
    self.location = location
    self.instructor = instructor
    self.ccn = ccn
    self.note = note
    self.description = description

  def __str__(self):
    return "Course:" + self.name +\
      "\nTitle:" + self.courseTitle +\
      "\nLocation:" + self.location +\
      "\nInstructor:" + self.instructor +\
      "\nCCN:" + self.ccn +\
      "\nNote:" + self.note +\
      "\nDescription:" + self.description + "\n"

def scrapeNC():
  """Scrape Ninja Course for a list of departments and codenames. 
  Some codenames are out of date though, e.g. L&S -> LNS"""

  url = "http://ninjacourses.com/explore/1/"
  r = requests.get(url)
  soup = BeautifulSoup(r.content, from_encoding="utf-8")
  left = soup.find("ul", {"id": "deptlist-left"})
  right = soup.find("ul", {"id": "deptlist-right"})
  text = left.text.strip() + "\n" + right.text.strip()
  return text

def writeAllDeptsToFile():
  """Write all depts scraped to a text file for later use"""
  text = scrapeNC()
  with open("list/dept.txt", "wb") as f:
    f.write(text)

def buildDictFromFile():
  courseDict = {}
  with open("list/dept.txt", "rb") as f:
    for line in f.readlines():
      line = line.strip()
      firstParen = line.find("(")
      lastParen = line.find(")")
      dept = line[:firstParen].strip()
      code = line[firstParen+1:lastParen].strip()
      courseDict[dept] = code

  with open("pickle/courseDict.pickle", "wb") as f:
    dump(courseDict, f)

def loadDictFromPickle():
  with open("pickle/courseDict.pickle", "rb") as f:
    courseDict = load(f)
    return courseDict

if __name__ == "__main__":
  print "haha... don't run util unless you know what you're doing"
  #buildDictFromFile()
  #loadDictFromPickle()
