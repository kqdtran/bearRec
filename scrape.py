import os
import shutil
import requests
import simplejson as sj
import collections as cl
from bs4 import BeautifulSoup
from cPickle import load, dump
from pprint import pprint
import util
from auth import authenticate


# Set your API keys here
appID, appKey = authenticate()

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
        result = sj.loads(req.content)['CanonicalDepartment']

        # Writes departmentCode to text file for later use
        with open("list/deptCode.txt", "a") as f:
            for dept in result:
                if 'departmentCode' in dept:
                    print "Writing to file department code", dept['departmentCode']
                    f.write(dept['departmentCode'] + "\n")

        # Writes departmentName to text file for later use
        with open("list/deptName.txt", "a") as f:
            for dept in result:
                if 'departmentName' in dept:
                    print "Writing to file department name", dept['departmentName']
                    f.write(dept['departmentName'] + "\n")


def getAllCoursesInDeptFromCatalog(deptCode='COMPSCI'):
    """
    Get all courses from the catalog given a department code
    """

    params = {'departmentCode': deptCode, 'app_id': appID, 
                        'app_key': appKey, '_type': 'json'}
    req = requests.get(urlCatalog, params=params)
    courses = []

    if req.status_code == 200:
        result = sj.loads(req.content)['CanonicalCourse']
        for course in result:
            if 'courseUID' in course and 'courseTitle' in course\
                 and 'courseNumber' in course and 'courseDescription' in course:
                course = util.CourseCatalog(course['courseUID'], course['courseTitle'],
                                                             course['courseNumber'], course['courseDescription'])
                courses.append(course)
    return courses


def getAllCoursesFromCatalog():
    """
    Get all courses from the catalog
    """

    allCourses = {}
    with open("list/deptCode.txt", "r") as f:
        deptCodeList = f.readlines()
        for deptCode in deptCodeList:
            deptCode = deptCode.strip()
            print "Processing dept", deptCode
            coursesInDept = getAllCoursesInDeptFromCatalog(deptCode)
            if coursesInDept:
                allCourses[deptCode] = coursesInDept
                print "Finish processing", len(coursesInDept), "courses\n"
            else:
                print "There are no courses under this department. Move on\n"

    # dump the catalog of every courses into a pickle file for later use
    with open("pickle/courseCatalog.pickle", "w") as f:
        print "Begin dumping all courses"
        dump(allCourses, f, 0)
        print "Finish!!!"


def loadCourseCatalog():
    """
    Load the course catalog from the pickle file, then proceed to 
    append all courses to a list and return that
    """

    with open("pickle/courseCatalog.pickle", "r") as f:
        allCoursesDict = load(f)
    return allCoursesDict


def checkCoursesBeingOffered(course, term, termYear):
    """
    Get all courses in a given department that are 
    offered in a given term and year
    """

    deptCode = course.UID + '.' + term + '.' + termYear
    params = {'app_id': appID, 'app_key': appKey, '_type': 'json'}
    url = urlCourse + '/' + deptCode + '/section/001'
    try:
        req = requests.get(url, params=params)
    except:
        print 'Request to check', course, "in", term, termYear, 'was not successful'
        return None
    if req.status_code == 200:
        courseInJSON = sj.loads(req.content)['ClassSection']

        # Retrieves the information
        if 'sectionMeetings' in courseInJSON:
            meeting = courseInJSON['sectionMeetings']

            if 'room' in meeting and 'building' in meeting:
                location = (str(meeting['room']) + ' ' + 
                                        str(meeting['building'])).strip()
            else:
                location = 'None'

            time = ''
            if 'meetingDay' in meeting:
                time += str(meeting['meetingDay']) + ' ' 
            if 'startTime' in meeting:
                time += str(meeting['startTime']) + ' '
            if 'endTime' in meeting:
                time += str(meeting['endTime'])
            time = time.strip()

            if 'instructorNames' in meeting:
                instructor = meeting['instructorNames']
            else:
                instructor = []

            course = util.Course(course.UID, course.number, course.title, location, time, 
                                            instructor, course.description)
            return course
    return None


def getAllCoursesInTerm(term=util.currentTerm, termYear=util.currentYear):
    """
    Get all courses in a given term for ALL departments
    """

    allCoursesDict = loadCourseCatalog()
    coursesList = []
    for dept in allCoursesDict:
        print "Processing department", dept
        for course in allCoursesDict[dept]:
            course = checkCoursesBeingOffered(course, term, termYear)
            if course:  # if it's offered in the given semester
                coursesList.append(course)
        print "Finish processing", dept, "\n"
    
    print "Begin dumping into pickle"
    with open("pickle/" + term + termYear + "courses.pickle", "w") as f:
        dump(coursesList, f)
    print "Finish getting data for", term, termYear


def loadAllCoursesInTerm(term=util.currentTerm, termYear=util.currentYear):
    """
    Load all courses in a given term from a pickle file
    """

    with open("pickle/" + term + termYear + "courses.pickle", "r") as f:
        coursesList = load(f)
        return coursesList


if __name__ == "__main__":
    while True:
        # TODO: better menu...
        choice = util.coerceToInt(raw_input("Choose a number between 1-3: "))
        if choice == 1:
            getAllDepartments()
            break
        elif choice == 2:
            getAllCoursesFromCatalog()
            break
        elif choice == 3:
            getAllCoursesInTerm()
            break
