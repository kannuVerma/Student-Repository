""" Author: Kannu Verma """

import unittest
from HW09_Kannu_Verma import University, Student, Instructor


class StudentTest(unittest.TestCase):

    def test__init__(self) -> None:
        student:Student = Student('123', 'Kannu', 'CS')
        self.assertEqual(student.cwid, '123')
        self.assertEqual(student.name, 'Kannu')
        self.assertEqual(student.major, 'CS')

    def test_add_course_grade(self) -> None:
        student:Student = Student('123', 'Kannu', 'CS')
        student.add_course_grade('SSW-810', 'A')
        self.assertEqual(student.pretty_table_output(), ['123', 'Kannu', ['SSW-810']])
        

class InstructorTest(unittest.TestCase):

    def test__init__(self) -> None:
        instructor:Instructor = Instructor('123', 'Kannu', 'CS')
        self.assertEqual(instructor.cwid, '123')
        self.assertEqual(instructor.name, 'Kannu')
        self.assertEqual(instructor.dept, 'CS')

    def test_course_taught(self) -> None:
        instructor:Instructor = Instructor('234', 'Taniya', 'CS')
        instructor.course_taught('CS-545')
        instructor.course_taught('CS-545')
        self.assertEqual(instructor.course_student_count, {'CS-545':2})


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)