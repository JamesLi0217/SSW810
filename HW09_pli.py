#!/usr/bin/env python
# coding=UTF-8
'''
@Author: Puzhuo Li
@Github: https://github.com/JamesLi0217
@Date: 2019-03-31 21:41:18
'''

import os
from collections import defaultdict
from prettytable import PrettyTable


class Student():
    '''to hold all of the details of a student'''

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = defaultdict(str)

    def add_grade(self, course_no, grade):
        ''' course : grade '''
        self.course[course_no] = grade

    def add_student_pt(self):
        ''' deliver row to repository'''
        return [self.cwid, self.name, sorted(self.course.keys())]

    def __str__(self):
        return f"cwid: {self.cwid}; name: {self.name}; major: {self.major}"


class Instructor():
    '''to hold all of the details of an instructor'''

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(int)

    def count_num(self, course_no):
        ''' course : number of students in the course'''
        self.course[course_no] += 1

    def add_instructor_pt(self):
        ''' deliver row to repository'''
        for course_name, student_num in self.course.items():
            yield self.cwid, self.name, self.dept, course_name, student_num

    def __str__(self):
        return f"cwid: {self.cwid}; name: {self.name}; dept: {self.dept}"


class Repository():
    '''to hold the students, instructors and grades'''

    def __init__(self, path):
        self.path = path
        self.students = {}
        self.instructors = {}
        self.add_students()
        self.add_instructors()
        self.add_courses()

    def file_reader(self, path, fields, sep="\t", header=False):
        '''Reading text files with a fixed number of fields,
        separated by a pre-defined character'''
        try:
            fp = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {path}")
        else:
            with fp:
                index = 0
                for line in fp:
                    index += 1
                    line = line.rstrip()
                    # false = skip first line
                    if header is False:
                        header = True
                        continue
                    if len(line.split(sep)) != fields:
                        raise ValueError(
                            f"{path} has {len(line.split(sep))} fields on line {index} but expected {fields}")
                    else:
                        yield list(line.split(sep, fields))

    def add_students(self):
        ''' to add student info'''
        path_student = os.path.join(self.path, r"students.txt")
        students_list = []
        for cwid, name, major in self.file_reader(path_student, 3, "\t", True):
            self.students[cwid] = Student(cwid, name, major)
            students_list.append(str(Student(cwid, name, major)))
        return students_list

    def add_instructors(self):
        ''' to add instructors info'''
        path_instructor = os.path.join(self.path, r"instructors.txt")
        instructor_list = []
        for cwid, name, dept in self.file_reader(path_instructor, 3, "\t", True):
            self.instructors[cwid] = Instructor(cwid, name, dept)
            instructor_list.append(str(Instructor(cwid, name, dept)))
        return instructor_list

    def add_courses(self):
        ''' to add courses info'''
        path_grades = os.path.join(self.path, r"grades.txt")

        for student_cwid, course_no, grade, instructor_cwid in self.file_reader(path_grades, 4, "\t", True):
            if student_cwid in self.students:
                self.students[student_cwid].add_grade(course_no, grade)

            if instructor_cwid in self.instructors:
                self.instructors[instructor_cwid].count_num(course_no)

        student_courses = list(
            f'{student_cwid}: {list(student.course)}' for student_cwid, student in self.students.items())
        courses_students_num = list(
            f'{instructor_cwid}: {list(instructor.course)}' for instructor_cwid, instructor in self.instructors.items())
        return student_courses, courses_students_num

    def student_table(self):
        '''Use PrettyTable to generate a summary table of all of the students'''
        out_list = []
        table1 = PrettyTable()
        table1.field_names = ["CWID", "Name", "Completed Course"]
        for i in self.students.values():
            table1.add_row(i.add_student_pt())
            out_list.append(i.add_student_pt())
        print(f"Student Summary\n{table1}")

        return out_list

    def instructors_table(self):
        '''Use PrettyTable to generate a summary table of each of the instructors'''
        out_list = []
        table2 = PrettyTable()
        table2.field_names = [
            "CWID", "Name", "Dept", "Course", "Students"]
        for i in self.instructors.values():
            for row in list(i.add_instructor_pt()):
                table2.add_row(row)
                out_list.append(row)

        print(f"Instructor Summary\n{table2}")
        return out_list


def main():
    #repo = Repository(r"D:\sit study\SSW810Py practice\HW\HW09")
    repo = Repository(r"./documents")
    repo.student_table()
    repo.instructors_table()


if __name__ == "__main__":
    main()
