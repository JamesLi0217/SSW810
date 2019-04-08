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


class Department():
    '''to hold the department, required and electives'''

    def __init__(self, dept):
        self.dept = dept
        self.required = []
        self.electives = []

    def add_req_course(self, course_no):
        '''store required info '''
        self.required.append(course_no)

    def add_ele_course(self, course_no):
        '''store electives info'''
        self.electives.append(course_no)

    def add_major_pt(self):
        '''deliver major info to major table'''
        return [self.dept, sorted(self.required), sorted(self.electives)]


class Student():
    '''to hold all of the details of a student'''

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = defaultdict(str)
        self.completed_courses = []
        self.remaining_requ = set()
        self.remaining_ele = set()

    def add_grade(self, course_no, grade):
        ''' course : grade '''
        self.course[course_no] = grade

    def progress_bar(self, department):
        '''for each student, add student' course info: completed_courses, remaining_required_course, remaining_electives'''
        all_courses = department.required + \
            department.electives + list(self.course.keys())

        for course_no in all_courses:
            if course_no in self.course and self.course[course_no] in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                self.completed_courses.append(course_no)

            elif course_no in department.required:
                self.remaining_requ.add(course_no)

        for course_no in department.electives:
            if course_no in self.completed_courses:
                self.remaining_ele = None
                break
        else:
            self.remaining_ele = set(department.electives)

    def add_student_pt(self):
        ''' deliver row to repository
        ["CWID", "Name", "Major","Completed Course", "Remaining Required", "Remaining Electives"]
        '''
        return [self.cwid, self.name, self.major, sorted(self.completed_courses), self.remaining_requ, self.remaining_ele]

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
        self.departments = {}
        self.add_students()
        self.add_instructors()
        self.add_courses()
        self.add_major()
        self.add_progress_bar()

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

    def add_major(self):
        ''' to add majors info'''
        path_grades = os.path.join(self.path, r"majors.txt")
        for dept, elec_req, course_no in self.file_reader(path_grades, 3, "\t", True):
            if dept not in self.departments:
                self.departments[dept] = Department(dept)

            if elec_req == "R":
                self.departments[dept].add_req_course(course_no)
            else:
                self.departments[dept].add_ele_course(course_no)

    def add_progress_bar(self):
        '''add process bar for each student'''
        for student in self.students.values():
            student.progress_bar(self.departments[student.major])

    def student_table(self):
        '''Use PrettyTable to generate a summary table of all of the students'''
        out_list = []
        table1 = PrettyTable()
        table1.field_names = ["CWID", "Name", "Major",
                              "Completed Course", "Remaining Required", "Remaining Electives"]
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

    def major_table(self):

        table3 = PrettyTable()
        table3.field_names = ["Dept", "Required", "Electives"]
        for i in self.departments.values():
            table3.add_row(i.add_major_pt())
        print(f"Majors Summary\n{table3}")


def main():
    repo = Repository(r"D:\sit study\SSW810Py practice\HW\HW09")
    repo = Repository(r"D:\download")
    #repo = Repository(r"/Users/daiyuping/Documents/GitHub/HW/HW09")
    repo.major_table()
    repo.student_table()
    repo.instructors_table()
    
    student1= Student("111","Tom","Software")
    student1.add_grade("SSW123", "A")
    student1.add_grade("SSW540", "A")
    student1.add_grade("SSW124", "C")
    student1.add_grade("SSW222", "E")
    a = Department("Software")
    student1.progress_bar(a)
    print(student1.add_student_pt())



if __name__ == "__main__":
    main()
