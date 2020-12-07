from flask import Flask, render_template
import sqlite3
from typing import Dict
from prettytable import PrettyTable

app: Flask = Flask(__name__)

DB_FILE: str = "C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-12\810_hw_12.db";

@app.route('/')
def student_details() -> str:
    query = 'select s.name as "Name", s.cwid as "CWID", g.course as "Course", g.grade as "Grade", i.name as "Instructor" from students s, grades g, instructors i where s.cwid=g.student_cwid and g.instructor_cwid=i.cwid order by s.name;'
    conn = sqlite3.connect(DB_FILE)

    data:List[Dict[str,str]] = [{'name':name, 'cwid':cwid, 'course':course, 'grade':grade, 'instructor':instructor} for name, cwid, course, grade, instructor in conn.execute(query)]
    conn.close()
    #return data
    return render_template('base.html', title='Stevens Repository', header='Student, Course, Grade, and Instructor', students=data)

app.run(debug=True)

