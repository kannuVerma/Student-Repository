""" Author: Kannu Verma """

from typing import DefaultDict
from HW08_Kannu_Verma import file_reader
from prettytable import PrettyTable
import os

"""" Holds all the information of Students, Instructors, grades of a University """
class University:

    def __init__(self):
        self.students = DefaultDict(str)
        self.instructors = DefaultDict(str)
        self.grades = list()

    # read student's file and save all data of student
    def read_students_file(self, path):
        for cwid, name, major in list(file_reader(path, 3, '\t')):
            if cwid not in self.students:
                self.students[cwid] = Student(cwid, name, major)
            else:
                print("Duplicate entry for a Student with cwid:"+cwid)

    # read student's file and save all data of instructor
    def read_instructors_file(self, path):
        for cwid, name, dept in list(file_reader(path, 3, '\t')):
            self.instructors[cwid] = Instructor(cwid, name, dept)

    # read student's file and save all data linked with student & Instructor
    def read_grades_file(self, path):
        for student_cwid, course, grade, instructor_cwid in list(file_reader(path, 4, '\t')):
            instructor_cwid = instructor_cwid.strip()
            
            #update the courses taken by each student, push course-grade dict for students
            self.students[student_cwid].add_course_grade(course, grade)
            #update the courses taught by each instructor and update the number of students
            self.instructors[instructor_cwid].course_taught(course)
    
    # prints students data
    def print_students(self):
        students_pretty_table:PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        for student in self.students.values():
            students_pretty_table.add_row(student.pretty_table_output())
        print(students_pretty_table)

    # prints Instructor data
    def print_instructors(self):
        instructors_pretty_table:PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Dept','Course', 'Students'])
        for instructor in self.instructors.values():
            for course in list(instructor.course_student_count.keys()):
                instructors_pretty_table.add_row([instructor.cwid, instructor.name, instructor.dept, course, instructor.course_student_count[course]])
        print(instructors_pretty_table)



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
    def pretty_table_output(self):
        return [self.cwid, self.name, sorted(list(self.courseGrade.keys()))]


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
    dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-9'
    university = University()
    university.read_students_file(os.path.join(dir_path, 'students.txt'))
    university.read_instructors_file(os.path.join(dir_path, 'instructors.txt'))
    university.read_grades_file(os.path.join(dir_path, 'grades.txt'))
    university.print_students()
    university.print_instructors()


if __name__ == '__main__':
    main()