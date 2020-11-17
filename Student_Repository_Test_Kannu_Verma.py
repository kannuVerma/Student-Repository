""" Author: Kannu Verma """

import unittest, os
from Student_Repository_Kannu_Verma import University, Student, Instructor


class UniversityTest(unittest.TestCase):
    
    # verify contents of majors table
    def test_majors_pretty_table(self) -> None:
        university = University()
        dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-10\Student-Repository'
        university.read_majors_file(os.path.join(dir_path, 'majors.txt'))
        self.assertEqual(list(university.major_req_courses.keys()), ['SFEN', 'SYEN'])
        self.assertEqual(list(university.major_req_courses.values()), [['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'], ['SYS 671', 'SYS 612', 'SYS 800'] ])
        self.assertEqual(list(university.major_elective_courses.values()),  [['CS 501', 'CS 513', 'CS 545'], ['SSW 810', 'SSW 565', 'SSW 540']])

    # verify contents of Student and Instructor table
    def test_student_instructor_pretty_table(self) -> None:
        university = University()
        dir_path:str = 'C:\KANNU\Stevens\Fall-2020\SSW-810\Assignment-10\Student-Repository'
        university.read_students_file(os.path.join(dir_path, 'students.txt'))
        university.read_instructors_file(os.path.join(dir_path, 'instructors.txt'))
        university.read_grades_file(os.path.join(dir_path, 'grades.txt'))
        self.assertEqual(len(university.students), 10)
        self.assertEqual(university.students['10103'].name, 'Baldwin, C')
        self.assertEqual(university.students['10103'].major, 'SFEN')
        self.assertEqual(list(university.students['10103'].courseGrade.keys()), ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501'])
        
        self.assertEqual(university.instructors['98764'].name, 'Feynman, R')
        self.assertEqual(university.instructors['98764'].cwid, '98764')
        self.assertEqual(university.instructors['98764'].dept, 'SFEN')
        self.assertEqual(len(university.instructors['98764'].course_student_count), 4)
        self.assertEqual(university.instructors['98764'].course_student_count['SSW 564'], 3)
        self.assertEqual(university.instructors['98764'].course_student_count['SSW 687'], 3)
        self.assertEqual(university.instructors['98764'].course_student_count['CS 501'], 1)
        self.assertEqual(university.instructors['98764'].course_student_count['CS 545'], 1)
        
        
        
        
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