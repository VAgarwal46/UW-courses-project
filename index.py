import os.path
import createDatabase 
import findCourse

if os.path.isfile('./coursesdb.sqlite') == False:
    db = createDatabase.createDatbase()
    print("DATABASE IS COMPLETE!")
else:
    db = createDatabase.existingDatabase()

#print(findCourse.courseListFilter(db,((3,4),0,6)))
#print(findCourse.courseListCourseNum(db,"CS200"))
#print(findCourse.courseListCourseTitle(db, "Computer engineering"))
