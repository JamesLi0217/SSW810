#!/usr/bin/env python
# coding=UTF-8
'''
@Author: Puzhuo Li
@Github: https://github.com/JamesLi0217
@Date: 2019-04-14 00:12:47
'''
import sqlite3
from prettytable import PrettyTable
DB_FILE = r"D:\download\sqlite-tools-win32-x86-3270200\HW11_pli.db"
db = sqlite3.connect(DB_FILE)


'''def creat_table():
    table_name = input("Please enter the table name: ")
    db.execute(f'create  table {table_name} (cwid varchar(10), name varchar(20), department varchar(10), course varchar(10), "number of students" int(2))')'''


def main():
    print("-"*20, 1, "-"*20)
    for row in db.execute('select Name from HW11_students where CWID = "11461"'):
        print(row)

    print("-"*20, 2, "-"*20)
    for row in db.execute('select major, count(*) as Number from HW11_majors group by Major'):
        print(row)

    print("-"*20, 3, "-"*20)
    for row in db.execute('select Grade, max(frequent) from (select  Grade, count(*) as frequent from HW11_grades group by Grade)'):
        print(row)

    print("-"*20, 4, "-"*20)
    for row in db.execute('select s.Name, s.CWID, s.Major, g.Course,g.Grade from HW11_students s join (select Student_CWID, Course, Grade from HW11_grades) g where s.CWID = g.Student_CWID'):
        print(row)

    print("-"*20, 5, "-"*20)
    for row in db.execute('select Name from (HW11_students s join (select Student_CWID, Course, Grade from HW11_grades where Course= "SSW 540") g on s.CWID = g.Student_CWID) where Grade is not null'):
        print(row)

    print("-"*20, 6, "-"*20)
    '''try:
        creat_table()
    except sqlite3.OperationalError:
        print("This table exist!")
    else:'''
    instructor_table = PrettyTable()
    instructor_table.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
    for row in db.execute('select  i.CWID,i.Name, i.Dept, g.Course,g.Number from (HW11_instructors i join (select count(*) as Number, Course, Instructor_CWID from HW11_grades group by Course) g on i.CWID = g.Instructor_CWID)'):
        instructor_table.add_row(list(row))
    print(f"Instructor Summary\n{instructor_table}")


if __name__ == "__main__":
    main()
