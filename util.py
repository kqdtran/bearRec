import requests
from bs4 import BeautifulSoup
from cPickle import load, dump


# Set the default semester and year here
currentTerm = "Fall"
currentYear = "2014"


class CourseCatalog():
    def __init__(self, UID, title, number, description):
        self.UID = UID
        self.title = title
        self.number = number
        self.description = description

    def __str__(self):
        return "UID:" + str(self.UID) +\
            "\nTitle:" + str(self.title) +\
            "\nNumber:" + str(self.number) +\
            "\nDescription:" + str(self.description) + "\n"


class Course():
    def __init__(self, UID, number, title, location, time, instructor, description, ccn=None, note=None):
        self.UID = UID
        self.number = number
        self.title = title
        self.location = location
        self.time = time
        self.instructor = instructor
        self.description = description
        self.ccn = ccn
        self.note = note

    def __str__(self):
        return "UID:" + str(self.UID) +\
            "\nCourse Number:" + str(self.number) +\
            "\nTitle:" + str(self.title) +\
            "\nLocation:" + str(self.location) +\
            "\nTime:" + str(self.time) +\
            "\nInstructor:" + str(self.instructor) +\
            "\nDescription:" + str(self.description) + "\n"


def coerceToInt(x):
        """
        Coerce x to type int, or exit the program
        """

        try:
                return int(x)
        except:
                return 0
