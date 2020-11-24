""" Author: Kannu Verma """

import unittest, os
from Student_Repository_Kannu_Verma import University, Student, Instructor


class UniversityTest(unittest.TestCase):
    
    # verify contents of majors table
    def test_majors_pretty_table(self) -> None:
        university = University()
        dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-11\Student-Repository'
        university.read_majors_file(os.path.join(dir_path, 'majors.txt'))
        self.assertEqual(list(university.major_req_courses.keys()), ['SFEN', 'CS'])
        self.assertEqual(list(university.major_req_courses.values()), [['SSW 540', 'SSW 810', 'SSW 555'], ['CS 570', 'CS 546']])
        self.assertEqual(list(university.major_elective_courses.values()),  [['CS 501', 'CS 546'], ['SSW 810', 'SSW 565']])

    # verify contents of Student and Instructor table
    def test_student_instructor_pretty_table(self) -> None:
        university = University()
        dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-11\Student-Repository'
        university.read_students_file(os.path.join(dir_path, 'students.txt'))
        university.read_instructors_file(os.path.join(dir_path, 'instructors.txt'))
        university.read_grades_file(os.path.join(dir_path, 'grades.txt'))
        self.assertEqual(len(university.students), 4)
        self.assertEqual(university.students['10103'].name, 'Jobs, S')
        self.assertEqual(university.students['10103'].major, 'SFEN')
        self.assertEqual(list(university.students['10103'].courseGrade.keys()), ['SSW 810', 'CS 501'])
        
        self.assertEqual(university.instructors['98764'].name, 'Cohen, R')
        self.assertEqual(university.instructors['98764'].cwid, '98764')
        self.assertEqual(university.instructors['98764'].dept, 'SFEN')
        self.assertEqual(len(university.instructors['98764'].course_student_count), 1)
        self.assertEqual(university.instructors['98764'].course_student_count['CS 546'], 1)
        self.assertEqual(university.instructors['98763'].course_student_count['SSW 810'], 4)
        self.assertEqual(university.instructors['98763'].course_student_count['SSW 555'], 1)
        self.assertEqual(university.instructors['98762'].course_student_count['CS 570'], 1)

    #New Test cases
    def test_student_grades_table_db(self) -> None:
        university = University()
        dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-11\Student-Repository'
        university.student_grades_table_db(os.path.join(dir_path, '810_hw_11.db'))
        self.assertEqual(university.students_grades[0], ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'))
        self.assertEqual(university.students_grades[1], ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'))
        
        
# Test cases for General Student information verification
class StudentTest(unittest.TestCase):

    def test__init__(self) -> None:
        student:Student = Student('123', 'Kannu', 'CS')
        self.assertEqual(student.cwid, '123')
        self.assertEqual(student.name, 'Kannu')
        self.assertEqual(student.major, 'CS')

    def test_student_pretty_table_content(self) -> None:
        student:Student = Student('123', 'Kannu', 'CS')
        student.add_course_grade('SSW-810', 'A')
        self.major_req_courses = {'CS':['SSW-810', 'CS-545', 'CS-548', 'CS-594']}
        self.major_elective_courses = {'CS': ['SSW-600', 'CS-501']}
        self.assertEqual(student.pretty_table_output(set(self.major_req_courses[student.major]), set(self.major_elective_courses[student.major])), ['123', 'Kannu', 'CS', ['SSW-810'], ['CS-545', 'CS-548', 'CS-594'], ['CS-501', 'SSW-600'], '4.0'])

class InstructorTest(unittest.TestCase):

    def test__init__(self) -> None:
        instructor:Instructor = Instructor('456', 'Taniya', 'SSW')
        self.assertEqual(instructor.cwid, '456')
        self.assertEqual(instructor.name, 'Taniya')
        self.assertEqual(instructor.dept, 'SSW')

    def test_course_taught(self) -> None:
        instructor:Instructor = Instructor('456', 'Taniya', 'SSW')
        instructor.course_taught('CS-545')
        instructor.course_taught('CS-545')
        instructor.course_taught('SSW-810')
        self.assertEqual(instructor.course_student_count, {'CS-545':2, 'SSW-810':1} )


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)