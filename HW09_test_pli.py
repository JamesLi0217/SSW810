#!/usr/bin/env python
# coding=UTF-8
'''
@Author: Puzhuo Li
@Github: https://github.com/JamesLi0217
@Date: 2019-04-01 21:49:03
'''
import os
import unittest
from HW09_pli import Student, Instructor, Repository

student1 = Student("10013", "Tom", "Software")
student1.course = {"SSW540": "A-", "SSW810": "A"}
student2 = Student("10099", "Jack", "System")
student2.course = {"SYS111": "", "SSW810": "A"}


class TestStudent(unittest.TestCase):
    def test_init(self):
        """ verify __init__() work properly """

        self.assertEqual(student1.cwid, "10013")
        self.assertEqual(student1.name, "Tom")
        self.assertEqual(student1.major, "Software")
        self.assertEqual(student1.course, {"SSW540": "A-", "SSW810": "A"})

    '''def test_add_grade(self):
        self.assertEqual()'''

    def test_add_student_pt(self):
        self.assertEqual(student1.add_student_pt(), [
                         '10013', 'Tom', ['SSW540', 'SSW810']])
        self.assertEqual(student2.add_student_pt(), [
                         '10099', 'Jack', ['SSW810', 'SYS111']])


instructor1 = Instructor("10086", "John", "Science")
instructor1.course = {"SSW540": 3, "SSW810": 7}


class TestInstructor(unittest.TestCase):
    def test_init(self):
        """ verify __init__() work properly """

        self.assertEqual(instructor1.cwid, "10086")
        self.assertEqual(instructor1.name, "John")
        self.assertEqual(instructor1.dept, "Science")
        self.assertEqual(instructor1.course, {"SSW540": 3, "SSW810": 7})

    '''def test_count_num(self):
        self.assertEqual()'''

    def test_add_instructor_pt(self):
        self.assertEqual(list(instructor1.add_instructor_pt()), [
                         ('10086', 'John', 'Science', 'SSW540', 3), ('10086', 'John', 'Science', 'SSW810', 7)])


#repo = Repository(r"D:\sit study\SSW810Py practice\HW\HW09")
repo = Repository(r"./documents")


class TestRepo(unittest.TestCase):
    def test_init(self):
        """ verify __init__() work properly"""

        '''with self.assertRaises(ValueError):
            #Repository(r"D:\sit study\SSW810Py practice\HW\HW09_error")
            Repository(r"./documents")'''
        with self.assertRaises(FileNotFoundError):
            Repository(r"D:\sit study\SSW810Py practice\HW\HW09_notexist")
        self.assertEqual(repo.path, r"D:\sit study\SSW810Py practice\HW\HW09")

    def test_file_reader(self):
        """ verify file_reader() work properly """

        path_student = os.path.join(repo.path, r"students.txt")
        self.assertEqual(list(repo.file_reader(path_student, 3, "\t", True)), [
                         ['10103', 'Baldwin, C', 'SFEN'], ['10115', 'Wyatt, X', 'SFEN']])

    def test_add_students(self):
        """ verify add_students() work properly """

        self.assertEqual(repo.add_students(), [
                         'cwid: 10103; name: Baldwin, C; major: SFEN', 'cwid: 10115; name: Wyatt, X; major: SFEN'])

    def test_add_instructors(self):
        """ verify add_instructors() work properly """

        self.assertEqual(repo.add_instructors(), [
                         'cwid: 98765; name: Einstein, A; dept: SFEN', 'cwid: 98764; name: Feynman, R; dept: SFEN'])

    def test_add_courses(self):
        """ verify add_courses() work properly """

        self.assertEqual(repo.add_courses(), (["10103: ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']", '10115: []'], [
                         "98765: ['SSW 567']", "98764: ['SSW 564', 'SSW 687', 'CS 501']"]))

    def test_student_table(self):
        """ verify student_table() work properly """
        #repo = Repository(r"D:\sit study\SSW810Py practice\HW\HW09")
        repo = Repository(r"./documents")

        '''self.assertEqual(repo.add_courses(), (["10103: ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']", '10115: []'], [
                         "98765: ['SSW 567']", "98764: ['SSW 564', 'SSW 687', 'CS 501']"]))'''
        self.assertEqual(repo.student_table(), [['10103', 'Baldwin, C', [
                         'CS 501', 'SSW 564', 'SSW 567', 'SSW 687']], ['10115', 'Wyatt, X', []]])

    def test_instructors_table(self):
        """ verify instructors_table() work properly """
        #repo = Repository(r"D:\sit study\SSW810Py practice\HW\HW09")
        repo = Repository(r"./documents")


        '''self.assertEqual(repo.add_courses(), (["10103: ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']", '10115: []'], [
                         "98765: ['SSW 567']", "98764: ['SSW 564', 'SSW 687', 'CS 501']"]))'''
        self.assertEqual(repo.instructors_table(), [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 2), ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 1), (
            '98764', 'Feynman, R', 'SFEN', 'SSW 687', 1), ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1)])


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
