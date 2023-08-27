#find by only filters
def courseListFilter(db, filters):
    #extract all rows from the database that have the filters as written in parameters
    return db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClauseFilters(filters))

#find by course name
def courseListCourseNum(db, name, filters = (0,0,0)):
    name = name.upper()
    courseNum = ""
    dept = ""
    #separating dept name and course nnumber from the course name
    for ch in name:
        if ch.isnumeric():
            courseNum += ch
        else:
            dept += ch
    dept = dept.strip()
    whereClause = f"courseNum = {courseNum} and deptAbbreviation = '{dept}'"
    #if there are any filters (gen-eds, breadths, level)
    if filters != (0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    try : 
        course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
        return course
    except: 
        print("COULDN'T FIND THE COURSE")
    
    ##IF GIVEN COURSE NAME DOES NOT EXIST
    print("DO YOU MEAN")

    #Trying to find course with dept name having more characters in it. eg. CS-(Comp Sci)
    deptLike = ""
    for ch in dept:
        deptLike += f"{ch}% "
    deptLike = deptLike.strip()
    whereClause = f"courseNum = {courseNum} and deptAbbreviation like '{deptLike}'"
    if filters != (0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    try:
        course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
        return course
    except:
        pass
    
    
    deptLike = f"{dept}%"
    whereClause = f"courseNum = {courseNum} and deptAbbreviation like '{deptLike}'"
    if filters != (0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    #print(whereClause)
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != []:
        return course

    deptLike = ""
    for ch in dept:
        deptLike += f"%{ch}"
    deptLike += '%'
    whereClause = f"courseNum = {courseNum} and deptAbbreviation like '{deptLike}'"
    if filters != (0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    #print(whereClause)
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != []:
        return course
    else:
        print("COULDN'T FIND WHAT YOU ARE LOOKING FOR")

#find by course title
def courseListCourseTitle(db, title, filters = (0,0,0)):
    title = title.upper()

    whereClause = f"courseTitle = '{title}'"
    if filters != (0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != []:
        return course
    
    titleWords = title.split()
    whereClause = "courseTitle like '"
    for word in titleWords:
        whereClause += f"%{word}"
    whereClause += "%'"
    if filters != (0,0,0):
        whereClause += f" and {whereClauseFilters(filters)}"
    #print(whereClause)
    course = db.extractValuesMultipleTables(("coursesTable", "deptNameTable"),
                                    "coursesTable.deptNameID = deptNameTable.id",
                                    ("deptAbbreviation", "CourseNum", "CourseTitle", "credits"),
                                    whereClause)
    #print(course)
    if course != []:
        return course

#where clause for filters
def whereClauseFilters(filters):
    whereClause = ""
    filtersName = ["genEdID", "breadthID", "levelID"]
    for i in range(3):
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


