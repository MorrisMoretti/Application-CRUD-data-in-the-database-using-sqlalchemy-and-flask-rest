from web_courses import CourseModel, GroupModel, StudentModel
from web_courses.api_courses import BaseManager
from web_courses.db_manager import PopulateDB

from .conftest import COURSE_LIST, GROUPS, STUDENTS, TABLES


def test_create_tables(empty_bd, drop_db):
    PopulateDB.create_tables()
    for table in TABLES:
        assert True is empty_bd.engine.has_table(table)


def test_pop_groups(use_db):
    PopulateDB.pop_groups(groups=GROUPS)
    results = BaseManager.session.query(GroupModel).all()
    for grop, result in zip(GROUPS, results):
        assert grop == result.to_dict()['name']


def test_pop_course(use_db):
    PopulateDB.pop_course(course_list=COURSE_LIST)
    results = BaseManager.session.query(CourseModel).all()
    for course, result in zip(COURSE_LIST, results):
        assert course == result.to_dict()['name']


def test_pop_students(db_manager_mock):
    query = PopulateDB.session.query(CourseModel).all()
    PopulateDB.pop_students(students=STUDENTS, courses=query)
    results = BaseManager.session.query(StudentModel).all()
    for student, result in zip(STUDENTS, results):
        student_vals = [student.name,
                        student.last_name,
                        student.id_group]
        result_vals = [result.to_dict()['first_name'],
                       result.to_dict()['last_name'],
                       result.to_dict()['id_group']]
        assert student_vals == result_vals
