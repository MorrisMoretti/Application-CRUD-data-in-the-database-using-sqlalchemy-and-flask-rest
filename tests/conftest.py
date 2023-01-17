from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from app import app as flask_app
from web_courses import Base, CourseModel, GroupModel, StudentModel
from web_courses.utils import NewStudent

COURSE_LIST = ['Python', 'Flask', 'Cli']
TABLES = ['association_table', 'Courses', 'Students', 'Groups']
GROUPS = ['AF-36', 'AG-99', 'AJ-80']
STUDENTS = [NewStudent(name='Billy', last_name='Garcia', id_group=1, course='Python'),
            NewStudent(name='James', last_name='Adams', id_group=2, course='Flask'),
            NewStudent(name='Tara', last_name='Stevenson', id_group=3, course='Cli')]
COUNT_ST = [{'id': 10, 'name': 'CP-33', 'students': 16},
            {'id': 2, 'name': 'QS-23', 'students': 17},
            {'id': 3, 'name': 'EB-65', 'students': 21}]
ALL_STUD = [{'id': '1', 'first_name': 'Richard', 'last_name': 'Durazo', 'id_group': 1},
            {'id': '2', 'first_name': 'Mattie', 'last_name': 'Vaughan', 'id_group': 1},
            {'id': '3', 'first_name': 'Roger', 'last_name': 'Wright', 'id_group': 9},
            {'id': '4', 'first_name': 'Larry', 'last_name': 'Kraemer', 'id_group': 1}]
COURSES = [{'id_course': 1, 'name': 'Python', 'description': 'This course is Python'},
           {'id_course': 3, 'name': 'Cli', 'description': 'This course is Cli'},
           {'id_course': 2, 'name': 'Flask', 'description': 'This course is Flask'}]


@pytest.fixture
def student_course_manager_mock():
    with patch('web_courses.api_courses.api_views.StudentCourseManager') as MockClass:
        yield MockClass


@pytest.fixture
def course_manager_mock():
    with patch('web_courses.api_courses.api_views.CourseManager') as MockClass:
        yield MockClass


@pytest.fixture
def student_manager_mock():
    with patch('web_courses.api_courses.api_views.StudentManager') as MockClass:
        yield MockClass


@pytest.fixture
def group_course_manager_mock():
    with patch('web_courses.api_courses.api_views.GropCourseManager') as MockClass:
        yield MockClass


@pytest.fixture()
def app():
    flask_app.config.from_object(config.TestConfig)
    with flask_app.app_context():
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture()
def empty_bd():
    with flask_app.app_context():
        flask_app.config.from_object(config.TestConfig)
        engine_db = create_engine(config.DB_URL)
        yield engine_db


@pytest.fixture
def use_db(empty_bd, app):
    with flask_app.app_context():
        flask_app.config.from_object(config.TestConfig)
        Base.metadata.create_all(empty_bd)
        session_db = sessionmaker(bind=empty_bd)
        yield session_db()
        session_db.close_all()
        Base.metadata.drop_all(empty_bd)


@pytest.fixture
def group_course_db(use_db):
    [use_db.add(GroupModel(name=group)) for group in GROUPS]
    [use_db.add(CourseModel(name=course,
                            description=f'This course is {course}')) for course in COURSE_LIST]
    use_db.commit()
    return use_db


@pytest.fixture
def db_manager_mock(group_course_db):
    with patch("web_courses.db_manager.PopulateDB.session",
               return_value=group_course_db):
        return group_course_db


@pytest.fixture
def student_group_course_db(group_course_db):
    for course, student in zip(COURSE_LIST, STUDENTS):
        new_student = StudentModel(first_name=student.name, last_name=student.last_name, id_group=student.id_group)
        new_course = group_course_db.query(CourseModel).filter_by(name='Flask').all()
        new_student.course.append(new_course.pop())
        group_course_db.add(new_student)
        group_course_db.commit()
    return use_db


@pytest.fixture
def base_manager_mock(student_group_course_db):
    with patch("web_courses.api_courses.courses_manager.BaseManager.session",
               return_value=student_group_course_db):
        return student_group_course_db


@pytest.fixture()
def drop_db(empty_bd):
    yield
    Base.metadata.drop_all(empty_bd)
