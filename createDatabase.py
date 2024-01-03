#==========================File Header=============================================================
'''
This file creates a database of all the courses that UW has to offer according to the courses page
of the UW guide. This database includes [Id of the DeptName, Course Number, Course Title, 
Pre-Requisites, Id of the GenEd, Id of the Breadth, Id of the Level, Credits offered, Description]
for every course. 

Only thing needed is to run the createDatabase() function of this file which creates the database
and returns a database object referring to that database. 
(It usually takes a runtime of approximately 80 sec)
'''
#==========================File Header=============================================================

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from database import sqlite

#==========================Function Header=========================================================
'''
Extracts the courses page of the UW guide and using its content, creates and returns 
a dictionary where keys are the names of the departments and the values are the links
to the pages containing their respective offered courses for the semester

RETURN:
    deptKeys(dict) - dict with departments as keys and their respective courses page as values

'''
#==========================Function Header=========================================================
def deptLinks():
    #extract content of the UW courses guide page as a string
    coursesFile = urllib.request.urlopen('https://guide.wisc.edu/courses').read()
    coursesPage = BeautifulSoup(coursesFile, 'html.parser')
    #manipulating coursespage string to extract department names and their courses page links
    coursesSubPage = coursesPage.find(id = "/courses/")
    depts = coursesSubPage.findAll('a')
    #dict which will contain dept names as keys and 
    #url of their respective courses pages as the value
    deptLinks = dict()
    for line in depts:
        dept = line.text
        if dept.__contains__("\u200b"):
            deptSplit = dept.split("\u200b")
            dept = ""
            for i in deptSplit:
                dept += i
        deptLinks[dept] = 'https://guide.wisc.edu' + line.get('href')
    return deptLinks
    
#==========================Function Header=========================================================
'''
This function creates a table in the given database using functions fro the database file. 
It creates 5 tables: (genEdTable, breadthTable, levelTable, deptNameTable, coursesTable).

PARAMS:
    db(sqlite(object created using database.py file)) - database to which these tables are to 
    be added
'''
#==========================Function Header=========================================================
def createTables(db):
    db.createTable('genEdTable', ["id INTEGER NOT NULL PRIMARY KEY UNIQUE", "genEd TEXT"])
    db.createTable('breadthTable', ["id INTEGER NOT NULL PRIMARY KEY UNIQUE", "breadth TEXT"])
    db.createTable('levelTable', ["id INTEGER NOT NULL PRIMARY KEY UNIQUE", "level TEXT"])
    db.createTable('deptNameTable', ["id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE",
                                    "deptName TEXT", "deptAbbreviation TEXT"])
    db.createTable('coursesTable', ["id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE",
                                    "deptNameID INTEGER", "CourseNum INTEGER", "CourseTitle TEXT",
                                    "preReqs TEXT", "GenEdID INTEGER", "EthnicSt BOOL", "breadthID INTEGER", 
                                    "levelID INTEGER", "credits TEXT", "description TEXT"])

#==========================Function Header=========================================================
'''
This function adds to the genEdTable, all possible genEds a course can have 
(Comm A, Comm B, QR-A, QR-B) along with one called 'None' (for courses that do not fall 
under any of these genEds). It also assigns a unique integer id to each within the table to connect
it to the main coursesTable.

PARAMS:
    db(sqlite(object created using database.py file)) - database in which GenEdTable exists
'''
#==========================Function Header=========================================================
def genEdTable(db):
    db.insertValues('genEdTable', ('id','genEd'), (1,'Communication Part A'))
    db.insertValues('genEdTable', ('id','genEd'), (2,'Communication Part B'))
    db.insertValues('genEdTable', ('id','genEd'), (3,'Quantitative Reasoning Part A'))
    db.insertValues('genEdTable', ('id','genEd'), (4,'Quantitative Reasoning Part B'))
    db.insertValues('genEdTable', ('id','genEd'), (5,'None'))

#==========================Function Header=========================================================
'''
This function adds to the breadthTable, all possible breadths a course can have 
(Bio Sci, Humanities, Literature, Natural Sci, Physical Sci, Social Sci, Humanities or Soc Sci) 
along with one called 'None' (for courses that do not fall under any of these breadths). It also 
assigns a unique integer id to each within the table to connect it to the main coursesTable.

PARAMS:
    db(sqlite(object created using database.py file)) - database in which breadthTable exists
'''
#==========================Function Header=========================================================
def breadthTable(db):
    db.insertValues('breadthTable', ('id','breadth'), (1,'Biological Sci'))
    db.insertValues('breadthTable', ('id','breadth'), (2,'Humanities'))
    db.insertValues('breadthTable', ('id','breadth'), (3,'Literature'))
    db.insertValues('breadthTable', ('id','breadth'), (4,'Natural Science'))
    db.insertValues('breadthTable', ('id','breadth'), (5,'Physical Sci'))
    db.insertValues('breadthTable', ('id','breadth'), (6,'Social Science'))
    db.insertValues('breadthTable', ('id','breadth'), (7,'Either Humanities or Social Science'))
    db.insertValues('breadthTable', ('id','breadth'), (8,'Either Biological Science or Social Science'))
    db.insertValues('breadthTable', ('id','breadth'), (9,'None'))

#==========================Function Header=========================================================
'''
This function adds to the lavelTable, all possible levels a course can have 
(Elementary, Intermediate, Advanced)  along with one called 'None' (for courses that do not fall 
under any of these levels). It also assigns a unique integer id to each within the table to 
connect it to the main coursesTable.

PARAMS:
    db(sqlite(object created using database.py file)) - database in which levelTable exists
'''
#==========================Function Header=========================================================
def levelTable(db):
    db.insertValues('levelTable', ('id','level'), (1,'Elementary'))
    db.insertValues('levelTable', ('id','level'), (2,'Intermediate'))
    db.insertValues('levelTable', ('id','level'), (3,'Advanced'))
    db.insertValues('levelTable', ('id','level'), (4,'None'))

#==========================Function Header=========================================================
'''
This function uses the given department name which includes the department abbreviation in bracket
and manipulates it to save the name and abbreviation in the deptNameTable and assign an incrementing
unique integer id to each within the table to connect it to the main coursesTable. 

PARAMS:
    db(sqlite(object created using database.py file)) - database in which deptNameTable exists
    dept(Str) - department name of the form [deptName(deptAbbreviation)]

RETURN:
    id (int) - id assigned to the department added to the deptNameTable (for further use to connect 
                it to the coursesTable)    
'''
#==========================Function Header=========================================================
def deptNameTable(db, dept):
    deptList = dept.split('(')
    deptName = deptList[0].strip()
    deptAbbrev = deptList[-1].split(')')[-2]
    db.insertValues('deptNameTable', ('deptName','deptAbbreviation'), (deptName,deptAbbrev))
    extractVal = db.extractValuesSingleTable('deptNameTable', 'id' , f"deptName = '{deptName}'")
    id = extractVal[0][0]
    return id

#==========================Function Header=========================================================
'''
This function adds a given department's courses to the coursesTable by using the information on
their courses page and assigns all course information of every course from the page to the table.
It uses the ids for level, breadth, deptName and genEds instead of the repeating values from their
respective tables. 
The course information included is [Id of the DeptName, Course Number, Course Title, Pre-Requisites,
Id of the GenEd, Id of the Breadth, Id of the Level, Credits offered, Description]

PARAMS:
    db(sqlite(object created using database.py file)) - database in which all the required tables
                                                             exists
    dept(Str) - department name of the form [deptName(deptAbbreviation)]
    deptLink(Str) - string of the url of the courses page of the given department
'''
#==========================Function Header=========================================================
def addDeptToDatabase(db, dept, deptLink):
    deptID = deptNameTable(db, dept)
    deptFile = urllib.request.urlopen(deptLink).read()
    deptPage = BeautifulSoup(deptFile, 'html.parser')
    subPage = deptPage.findAll(class_ = 'courseblock')
    for courseBlock in subPage:
        course = courseBlock.find(class_ = 'courseblocktitle').text
        courseNum = -1
        for i in course.split():
            if i.isnumeric():
                courseNum = int(i)
                break
        courseTitle = course.split('—')[1].strip().upper()
        credits = courseBlock.find(class_ = 'courseblockcredits').text
        credits = credits.split()[0].strip()
        desc = courseBlock.find(class_ = 'courseblockdesc').text
        descDisform = desc.split('"')
        desc = descDisform[0]
        for i in range(1,len(descDisform)):
            desc += f"'{descDisform[i]}"
        desc = desc.strip()
        extras = courseBlock.find(class_ = 'cb-extras')
        extralist = extras.findAll(class_ = 'courseblockextra')
        req = "None"
        genEdID = 5
        breadthID = 9
        levelID = 4
        ethnicSt = 0
        for extra in extralist:
            extraStr = extra.text
            if extraStr.__contains__("Requisite"):
                req = extraStr.split(':')[1].strip()
            if extraStr.__contains__("Gen Ed"):
                genEdTable = db.extractValuesSingleTable('genEdTable')
                for value in genEdTable:
                    if extraStr.__contains__(value[1]):
                        genEdID = value[0]
            if extraStr.__contains__("Breadth"):
                breadthTable = db.extractValuesSingleTable('breadthTable')
                for value in breadthTable:
                    if extraStr.__contains__(value[1]):
                        breadthID = value[0]
            if extraStr.__contains__("Level"):
                levelTable = db.extractValuesSingleTable('LevelTable')
                for value in levelTable:
                    if extraStr.__contains__(value[1]):
                        levelID = value[0]
            if extraStr.__contains__("Ethnic St"):
                ethnicSt += 1
        db.insertValues('coursesTable', 
                        ('deptNameID', 'courseNum','courseTitle','credits','description','preReqs','genEdID','ethnicSt','breadthID','levelID'),
                        (deptID, courseNum,courseTitle,credits,desc,req,genEdID,ethnicSt,breadthID,levelID))
        ##print(courseNum)

#==========================Function Header=========================================================
'''
This function creates a database object(using the database class for database.py), uses the 
createTables(db), genEdTable(db), breadthTable(db), levelTable(db) functions from this file to
create the required database. It then uses the deptLinks() and parses the dict it produces to 
add all the courses offered to the database using the addDeptDatabase(db,dept,deptLink) function. 

RETURN:
    dbase(database(object created using database.py file)) - a database of all courses offered in 
                                                                a semester in a file named 
                                                                'coursesdb.sqlite'
'''
#==========================Function Header=========================================================
def createDatabase():
    dbase = sqlite('coursesdb')
    createTables(dbase)
    genEdTable(dbase)
    breadthTable(dbase)
    levelTable(dbase)
    deptLinksList = deptLinks()
    for dept in deptLinksList.keys():
        addDeptToDatabase(dbase, dept, deptLinksList[dept])
    return dbase

def existingDatabase():
    dbase = sqlite('coursesdb')
    return dbase