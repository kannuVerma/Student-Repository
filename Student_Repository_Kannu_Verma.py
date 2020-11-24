""" Author: Kannu Verma """

from typing import DefaultDict
from HW08_Kannu_Verma import file_reader
from prettytable import PrettyTable
import os
import sqlite3

"""" Holds all the information of Students, Instructors, grades of a University """
class University:

    def __init__(self):
        self.students = DefaultDict(str)
        self.instructors = DefaultDict(str)
        self.grades = list()
        self.major_req_courses = DefaultDict(list)
        self.major_elective_courses = DefaultDict(list)
        self.students_grades = list()

    # read student's file and save all data of student
    def read_students_file(self, path):
        for cwid, name, major in list(file_reader(path, 3, '\t', True)):
            if cwid not in self.students:
                self.students[cwid] = Student(cwid, name, major)
            else:
                print("Duplicate entry for a Student with cwid:"+cwid)

    # read student's file and save all data of instructor
    def read_instructors_file(self, path):
        for cwid, name, dept in list(file_reader(path, 3, '\t', True)):
            self.instructors[cwid] = Instructor(cwid, name, dept)

    # read student's file and save all data linked with student & Instructor
    def read_grades_file(self, path):
        for student_cwid, course, grade, instructor_cwid in list(file_reader(path, 4, '\t', True)):
            instructor_cwid = instructor_cwid.strip()
            
            #update the courses taken by each student, push course-grade dict for students
            self.students[student_cwid].add_course_grade(course, grade)
            #update the courses taught by each instructor and update the number of students
            self.instructors[instructor_cwid].course_taught(course)
    
    # read the majors file and calculate the remaining required and elective classes for each student
    def read_majors_file(self, path):
        for major, req_or_elective_flag, course in list(file_reader(path, 3, '\t', True)):
            if req_or_elective_flag == 'R':
                self.major_req_courses[major].append(course)
            elif req_or_elective_flag == 'E':
                self.major_elective_courses[major].append(course)
        
            
    # prints students data
    def print_students(self):
        students_pretty_table:PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remanining Required', 'Remaining Electives', 'GPA'])
        for student in self.students.values():
            students_pretty_table.add_row(student.pretty_table_output(set(self.major_req_courses[student.major]), set(self.major_elective_courses[student.major])))
        print(students_pretty_table)

    # prints Instructor data
    def print_instructors(self):
        instructors_pretty_table:PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Dept','Course', 'Students'])
        for instructor in self.instructors.values():
            for course in list(instructor.course_student_count.keys()):
                instructors_pretty_table.add_row([instructor.cwid, instructor.name, instructor.dept, course, instructor.course_student_count[course]])
        print(instructors_pretty_table)

    def print_majors(self):
        majors_pretty_table:PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Electives'])
        for major in self.major_req_courses:
            majors_pretty_table.add_row([major, sorted(list(self.major_req_courses[major])), sorted(list(self.major_elective_courses[major]))])
        print(majors_pretty_table)

    #new pretty table HW#11
    def student_grades_table_db(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for row in c.execute('select s.name as "Name", s.cwid as "CWID", g.course as "Course", g.grade as "Grade", i.name as "Instructor" from students s, grades g, instructors i where s.cwid=g.student_cwid and g.instructor_cwid=i.cwid order by s.name;'):
            self.students_grades.append(row)
        self.student_grades_pretty_table()


    def student_grades_pretty_table(self):
        students_grades_pretty_table:PrettyTable = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])
        for row in self.students_grades:
            students_grades_pretty_table.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(students_grades_pretty_table)


""" Holds all of the details of a student """
class Student:

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courseGrade = DefaultDict(str)

    # stores student course-grade information in a Dict
    def add_course_grade(self, course, grade):
        self.courseGrade[course] = grade

    # returns the data row wise for student' pretty table 
    def pretty_table_output(self, major_req_courses, major_elective_courses):
        gradeGpaMaping:DefaultDict = {'A':4, 'A-':3.75, 'B+':3.25, 'B':3, 'B-':2.75, 'C+': 2.25, 'C':2, 'C-':0, 'D+':0, 'D':0, 'D-':0, 'F':0}
        gpa:int = 0
        for grade in self.courseGrade.values():
            gpa = gpa + gradeGpaMaping.get(grade)
        
        return [self.cwid, self.name, self.major, sorted(list(self.courseGrade.keys())), sorted(major_req_courses - set(self.courseGrade.keys())), sorted(major_elective_courses - set(self.courseGrade.keys())), str(round(gpa/len(list(self.courseGrade.keys())), 2))]


""" Holds all of the details of an instructor """
class Instructor:

    def __init__(self, cwid, name, dept):
        self.name = name
        self.cwid = cwid
        self.dept = dept
        self.course_student_count = DefaultDict(int)
    
    # stores Instructor course-student's count information in a Dict
    def course_taught(self, course):
        self.course_student_count[course] += 1

""" Main Method """        
def main():
    dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-11\Student-Repository'
    university = University()
    university.read_majors_file(os.path.join(dir_path, 'majors.txt'))
    university.read_students_file(os.path.join(dir_path, 'students.txt'))
    university.read_instructors_file(os.path.join(dir_path, 'instructors.txt'))
    university.read_grades_file(os.path.join(dir_path, 'grades.txt'))
    print('\nMajors Summary')
    university.print_majors()
    print('\nStudent Summary')
    university.print_students()
    print('\nInstructor Summary')
    university.print_instructors()
    print('\nStudent Grade Summary')
    university.student_grades_table_db(os.path.join("C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-11\Student-Repository\810_hw_11.db"))


if __name__ == '__main__':
    main()