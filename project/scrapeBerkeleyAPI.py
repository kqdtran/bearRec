import requests
import simplejson as sj
from bs4 import BeautifulSoup
from cPickle import load, dump
from pprint import pprint
from util import Course


# Set your API keys here
appID = '613908b6'
appKey = 'e80bc3bd7672dbdfd9ce4d3827c4349a'

# URLs for requesting with Berkeley API
urlDept = "https://apis-dev.berkeley.edu/cxf/asws/department"
urlCourse = "https://apis-dev.berkeley.edu/cxf/asws/classoffering"
urlCatalog = "https://apis-dev.berkeley.edu/cxf/asws/course"

def getAllDepartments():
  """
  Get all departments in Berkeley and cache them
  """

  # X-tension courses are omitted
  alphabetString = "ABCDEFGHIJKLMNOPQRSTUVWYZ".lower()
  alphabet = list(alphabetString)
  for letter in alphabet:
    params = {'departmentCode': letter, 'app_id': appID, 
              'app_key': appKey, '_type': 'json'}
    req = requests.get(urlDept, params=params)
    deptStartWithThisLetter =\
      sj.loads(req.content)['CanonicalDepartment']\

    # Write departmentCode to text file for later use
    with open("list/deptCode.txt", "a") as f:
      for dept in deptStartWithThisLetter:
        if 'departmentCode' in dept:
          print "Writing to file department code", dept['departmentCode']
          f.write(dept['departmentCode'] + "\n")

    # Write departmentName to text file for later use
    with open("list/deptName.txt", "a") as f:
      for dept in deptStartWithThisLetter:
        if 'departmentName' in dept:
          print "Writing to file department name", dept['departmentName']
          f.write(dept['departmentName'] + "\n")

def getCoursesInDept(deptCode='COMPSCI', term='Spring', termYear='2014'):
  """
  Get all courses in a given department, term, and year
  """

  params = {'departmentCode': deptCode, 'term': term, 
            'termYear': termYear, 'app_id': appID, 
            'app_key': appKey, '_type': 'json'}
  req = requests.get(urlCourse, params=params)
  courses = sj.loads(req.content)['ClassOffering']
  
  for course in courses:
    print course
    break

def getAllCoursesInTerm(term='Spring', termYear='2014'):
  """
  Get all courses in a given term for ALL departments
  """

  with open("list/deptCode.txt", "r") as f:
    deptCodeList = f.readlines()
    for deptCode in deptCodeList:
      deptCode = deptCode.strip()
      coursesInDept = getCoursesInDept()
      break

def getCatalogDescription(deptCode='COMPSCI', courseNumber='61A'):
  """
  Get catalog description from a given department code and course number
  """
  
  pass

if __name__ == "__main__":
  #getAllDepartments()
  getAllCourses()
