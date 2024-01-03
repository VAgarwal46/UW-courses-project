import os
import createDatabase 
import findCourse
import time

def mainMenu():
    if os.path.isfile('./coursesdb.sqlite'):
        db = createDatabase.existingDatabase()
    else:
        db = createDatabase.createDatabase()
    while (True):
        print("MAIN MENU\n")
        datetime = accessDate()
        print(f"1. Update Database (will take upto 70-80 secs; last updated on {datetime})")
        print("2. Search for a course")
        print("3. View your four year plan(s)")
        print("4. Exit program")
        choice = int(input("Enter your choice(index no): "))
        print()
        if choice == 1:
            os.remove('./coursesdb.sqlite')
            db = createDatabase.createDatabase()
            print("DATABASE HAS BEEN UPDATED!")
        elif choice == 2:
            exitBool = searchMenu(db)
            if exitBool:
                break
        elif choice == 3:
            fourYearPlanMenu()
        elif choice == 4:
            break
        else:
            print("Action doesn't exist! Try Again")
        print()
    
def accessDate():
    try:
        timestamp  = time.ctime(os.path.getctime('./coursesdb.sqlite'))
        timestamp = timestamp.split()
        date = f"{timestamp[1]} {timestamp[2]},{timestamp[4]}"
        timeStr = timestamp[3]
        return (date, timeStr)
    except:
        return None

def searchMenu(db):
    while True:
        print("SEARCH MENU")
        print()
        print("1. Search using Course Name")
        print("2. Search using Department Name")
        print("3. Search using Course Number")
        print("4. Search using Course Title")
        print("5. Search using only filters")
        print("6. Go back to Main Menu")
        print("7. Exit program")
        choice = int(input("Enter your choice(index no): "))
        if choice == 1:
            name = input("\nCourse Name: ")
            filters = filterMenu()
            courseList = findCourse.courseListCourseName(db, name, filters)
            if courseList == None:
                print("TRY AGAIN!")
                continue
            print(courseList)
        elif choice == 2:
            name = input("\nDepartment Name/Abbreviation: ")
            filters = filterMenu()
            courseList = findCourse.courseListDeptName(db, name, filters)
            if courseList == None:
                print("TRY AGAIN!")
                continue
            print(courseList)
        elif choice == 3:
            num = int(input("\nCourse Number: "))
            filters = filterMenu()
            courseList = findCourse.courseListCourseNum(db, num, filters)
            if courseList == None:
                print("TRY AGAIN!")
                continue
            print(courseList)
        elif choice == 4:
            title = input("\nCourse Title: ")
            filters = filterMenu()
            courseList = findCourse.courseListCourseTitle(db, title, filters)
            if courseList == None:
                print("TRY AGAIN!")
                continue
            print(courseList)
        elif choice == 5:
            filters = filterMenu()
            courseList = findCourse.courseListFilter(db, filters)
            if courseList == None:
                print("TRY AGAIN!")
                continue
            print(courseList)
        elif choice == 6:
            pass
        elif choice == 7:
            return 1
        else:
            print("Wrong Input! Try again")
            continue
        return 0

def fourYearPlanMenu():
    print("4-year plan Menu")
    return

def filterMenu(existingFilters = (0,0,0,0)):
    filters = list(existingFilters)
    while True:
        print()
        genEd = ["Communication Part A", "Communication Part B", "Quantitative Reasoning Part A",
                "Quantitative Reasoning Part B"]
        breadth = ["Bio Sci", "Humanities", "Literature", "Natural Sci", "Physical Sci", "Social Sci"]
        level = ["Elementary", "Intermediate", "Advanced"]
        print("GEN-EDs")
        count = 1
        for i in range(len(genEd)):
            print(f"{count}. {genEd[i]}")
            count += 1
        print()
        print(f"{count}. Ethnic St")
        count += 1
        print("\nBREADTH")
        for i in range(len(breadth)):
            print(f"{count}. {breadth[i]}")
            count += 1
        print("\nLEVEL")
        for i in range(len(level)):
            print(f"{count}. {level[i]}")
            count += 1
        print()
        print(f"{count}. No Filter")
        choice = int(input("Enter your choice(index no): "))
        if choice > 0 and choice <= 4:
            if isinstance(filters[0], tuple):
                filters[0] += (choice, )
            else:
                filters[0] = (choice, )
        elif choice == 5:
            filters[1] = 1
        elif choice == 6:
            if isinstance(filters[2], tuple):
                filters[2] += (1,8)
            else:
                filters[2] = (1,8)
        elif choice == 7:
            if isinstance(filters[2], tuple):
                filters[2] += (2,7)
            else:
                filters[2] = (2,7)
        elif choice <= 10:
            if isinstance(filters[2], tuple):
                filters[2] += (choice-5, )
            else:
                filters[2] = (choice-5, )
        elif choice == 11:
            if isinstance(filters[2], tuple):
                filters[2] += (6,7,8)
            else:
                filters[2] = (6,7,8)
        elif choice <= 14:
            if isinstance(filters[3], tuple):
                filters[3] += (choice-11, )
            else:
                filters[3] = (choice-11, )
        elif choice == 15:
            return tuple(filters)
        else:
            print("Wrong Input! Try again")
            continue
        break
        
    print("\n")
    while True:
        print("1. Add another filter")
        print("2. SEARCH")

        choice = int(input("Enter your choice(index no): "))
        if choice == 1:
            return filterMenu(tuple(filters))
        elif choice == 2:
            return tuple(filters)
        else:
            print("Wrong Input! Try again")