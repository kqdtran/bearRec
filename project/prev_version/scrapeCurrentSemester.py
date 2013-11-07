import requests
from bs4 import BeautifulSoup
from cPickle import load, dump
from util import Course


def getURLFromDept(dept, term):
  """Get the URL on schedule.berkeley.edu for a given department
  in a given term.
  This is pretty hacky since I know the format of the url :p..."""

  dept = dept.strip().replace(" ", "+")
  url = 'http://osoc.berkeley.edu/OSOC/osoc?p_term={term}&x=58&p_classif=' +\
    '--+Choose+a+Course+Classification+--&p_deptname={dept}&p_presuf=--' +\
    '+Choose+a+Course+Prefix%2fSuffix+--&y=0'
  url = url.format(term=term, dept=dept)
  print url
  return url

def getCourseFromURL(url):
  """Get all the courses from a given URL using BeautifulSoup"""
  allCoursesFromURL = []
  r = requests.get(url)
  soup = BeautifulSoup(r.content, from_encoding="utf-8")
  url = "http://osoc.berkeley.edu/catalog/gcc_search_sends_request"

  # Bunch of list to keep track of what I scrape haha
  ccns = []
  courses = []
  titles = []
  notes = []
  instructors = []
  locations = []

  # Now then, shall we carry out everyone's favorite statement? FOR LOOP
  for sp in soup.find_all("tr"):
    text = sp.text.strip()
    notesAdded = False
    info = text[text.find(':')+1:].strip()
    if info:
      if "Course Title" in text:
        titles.append(info)
        validClass = True # start of a valid class
      elif "Location" in text:
        locations.append(info)
      elif "Instructor" in text:
        instructors.append(info)
      elif "Course Control Number" in text:
        ccns.append(info)
      elif "Note" in text:
        notes.append(info)
        notesAdded = True

      # Course Control Number and Course Title are already taken care of
      elif "Course" in text:
        courses.append(info)
        if not notesAdded:
          notes.append("")
          notesAdded = False

  # Get the description of each course extracted above
  descriptions = []
  for info in soup.find_all("form", 
                            {"action": "/catalog/gcc_search_sends_request"}):
    info = str(info.contents[0])
    index = info.find("<tr>")
    info = info[:index]

    matches = re.findall('value="([^">]*)', info)
    if len(matches) >= 3:
      params = {"p_dept_cd": matches[0], "p_title": matches[1], 
                "p_number": matches[2]}
      r = requests.post(url, params=params)
      soup = BeautifulSoup(r.content, from_encoding="utf-8")
      for desc in soup.find_all("font", {"size": -1}):
        desc = desc.text
        if "Description" in desc:
          desc = desc[desc.find(":")+1:].strip()
          descriptions.append(desc)

  # Finally, build a list of all classes... and pickle them
  for name, title, location, instructor, ccn, note, description in\
      zip(courses, titles, locations, instructors, ccns, notes, descriptions):

    # we don't care about discussion/lab, and only grab the first lecture section
    if ("LEC" in name or "SEM" in name) and "P 001" in name:
      course = Course(name, title, location, instructor, ccn, note, description)
      allCoursesFromURL.append(course)
  return allCoursesFromURL

def getAllCourses(term="SP", year=14):
  with open("list/dept.txt", "rb") as f:
    deptList = f.readlines()
    courseList = []
    i = 1
    for dept in deptList:
      if i == 50: break
      print "Processing department: " + dept
      url = getURLFromDept(dept, term)
      #courses = getCourseFromURL(url)
      #courseList.extend(courses)
      #print "Finish processing " + str(len(courses)) + " courses"
      print "---------------------"
      print
      i += 1

  # dump all the courses into one big pickle file
  with open("pickle/allCourses" + term + str(year) + ".pickle", "wb") as f:
    dump(courseList, f)
    print "------------------"
    print "Finish processing. Found " + str(len(courseList)) + " courses"
    print "------------------"

def loadAllCourses(term="SP"):
  courseList = None
  if term == "SP":
    with open("pickle/allCoursesSP14.pickle", "rb") as f:
      courseList = load(f)
  elif term == "FL":
    with open("pickle/allCoursesFA13.pickle", "rb") as f:
      courseList = load(f)
  return courseList

if __name__ == "__main__":
  getAllCourses()
