#find by only filters
def courseListFilter(db, filters):
    #extract all rows from the database that have the filters as written in parameters
    return db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClauseFilters(filters))

#find by course name
def courseListCourseName(db, name, filters = (0,0,0,0)):
    name = name.upper()
    courseNum = ""
    dept = ""
    #separating dept name and course number from the course name
    for ch in name:
        if ch.isnumeric():
            courseNum += ch
        else:
            dept += ch
    dept = dept.strip()
    whereClause = f"courseNum = {courseNum} and deptAbbreviation = '{dept}'"
    #if there are any filters (gen-eds, breadths, level)
    if filters != (0,0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    try : 
        course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
        if course == None or course == "" or course == []:
            pass
        else:
            return course
    except: 
        pass
    
    ##IF GIVEN COURSE NAME DOES NOT EXIST

    depts = db.extractValuesSingleTable("deptNameTable", "deptAbbreviation", f"deptAbbreviation = '{dept}'")
    if depts != None and depts != "" and depts != []:
        print("DO YOU MEAN")
        return courseListDeptName(db, dept, filters)
    
    #Trying to find course with dept name having more characters in it. eg. CS-(Comp Sci)
    deptLike = ""
    for ch in dept:
        deptLike += f"%{ch}% "
    deptLike = deptLike.strip()
    whereClause = f"courseNum = {courseNum} and deptAbbreviation like '{deptLike}'"
    if filters != (0,0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    try:
        course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
        if course == None or course == "" or course == []:
            print("COULDN'T FIND ANY SUCH COURSE")
        else:
            print("DO YOU MEAN")
            return course
    except:
        print("COULDN'T FIND ANY SUCH COURSE")

def courseListDeptName(db, name, filters = (0,0,0,0)):
    name = name.upper().strip()
    deptAbbrevs = db.extractValuesSingleTable("deptNameTable", "deptAbbreviation",f"deptAbbreviation = '{name}'")
    depts = db.extractValuesSingleTable("deptNameTable", "deptName",f"deptAbbreviation = '{name}'")
    if (deptAbbrevs != None and deptAbbrevs != "" and deptAbbrevs != []):
        whereClause = f"deptAbbreviation = '{name}'"
    elif depts != None and depts != "" and depts != []:
        whereClause = f"deptName = '{name}'"
    else:
        deptLike = ""
        for ch in name:
            deptLike += f"%{ch}% "
        deptLike = deptLike.strip()
        deptAbbrevs = db.extractValuesSingleTable("deptNameTable", "deptAbbreviation",f"deptAbbreviation like '{deptLike}'")
        depts = db.extractValuesSingleTable("deptNameTable", "deptName",f"deptAbbreviation like '{deptLike}'")
        if (deptAbbrevs != None and deptAbbrevs != "" and deptAbbrevs != []):
            whereClause = f"deptAbbreviation like '{deptLike}'"
        elif depts != None and depts != "" and depts != []:
            whereClause = f"deptName like '{deptLike}'"
        else:
            print("COUNDN'T FIND THE DEPARTMENT. RECHECK THE ENTERED NAME")
            return
    if filters != (0,0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    try : 
        course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
        if course == None or course == "" or course == []:
            print("COULDN'T FIND ANY COURSE")
        else:
            return course
    except: 
        print("COULDN'T FIND ANY COURSE")

def courseListCourseNum(db, num, filters = (0,0,0,0)):
    whereClause = f"courseNum = {num}"
    if filters != (0,0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != [] and course != None:
        return course
    print("COULDN'T FIND ANY COURSE FOR THAT COURSE NUMBER")

#find by course title
def courseListCourseTitle(db, title, filters = (0,0,0,0)):
    title = title.upper()

    whereClause = f"courseTitle = '{title}'"
    if filters != (0,0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != [] and course != None:
        return course
    
    titleWords = title.split()
    whereClause = "courseTitle like '"
    for word in titleWords:
        whereClause += f"%{word}"
    whereClause += "%'"
    if filters != (0,0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    #print(whereClause)
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != [] and course != None:
        return course
    print("COULDN'T FIND ANY COURSE WITH THE GIVEN TITLE")

#where clause for filters
def whereClauseFilters(filters):
    whereClause = ""
    filtersName = ["genEdID", "EthnicSt", "breadthID", "levelID"]
    for i in range(4):
        if filters[i] != 0:
            if isinstance(filters[i],int):
                if whereClause != "":
                    whereClause += " AND "
                whereClause += f"{filtersName[i]} = {filters[i]}"
            else:
                if whereClause != "":
                    whereClause += " AND "
                whereClause += f"({filtersName[i]} = {filters[i][0]}"
                for j in range(1,len(filters[i])):
                    whereClause += f" OR {filtersName[i]} = {filters[i][j]}"
                whereClause += ")"
    return whereClause
