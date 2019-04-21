#!/usr/bin/env python
# coding=UTF-8
'''
@Author: Puzhuo Li
@Github: https://github.com/JamesLi0217
@Date: 2019-04-20 22:13:53
'''
from flask import Flask, render_template
import sqlite3
app = Flask(__name__)


@app.route("/")
def students_summary():
    query = """select s.cwid, s.name, s.major, count(g.Course) as complete from HW11_students s join HW11_grades g on s.cwid = g.Student_CWID group by s.cwid, s.name, s.major"""
    db = sqlite3.connect(r"D:\Github\SSW810\HW11_pli.db")
    results = db.execute(query)
    data = [{"cwid": cwid, "name": name, "major": major, "complete": complete}
            for cwid, name, major, complete in results]
    db.close()
    return render_template("student_courses.html", title="HW12", table_title="Stevens Repository", comment="Number of students by course and instructor", students=data)


app.run(debug=True)
