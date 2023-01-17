import pytest

from tests.conftest import COURSE_LIST, GROUPS, STUDENTS
from web_courses.api_courses.courses_manager import (CourseManager,
                                                     GropCourseManager,
                                                     StudentCourseManager,
                                                     StudentManager)


def test_group_count_students(base_manager_mock):
    for result in GropCourseManager.group_count_students():
        assert result['name'] in GROUPS


def test_all_students(base_manager_mock):
    for result, student in zip(StudentManager.all_students(), STUDENTS):
        assert student.name == result['first_name']
        assert student.last_name == result['last_name']
        assert student.id_group == result['id_group']


def test_find_student_by_id(base_manager_mock):
    result = StudentManager.find_student_by_id(student_id='3')
    student = STUDENTS[2]
    assert student.name == result['first_name']
    assert student.last_name == result['last_name']
    assert student.id_group == result['id_group']


@pytest.mark.parametrize('param, expected_result',
                         [('3', '3'),
                          ('30', None)])
def test_drop_student_by_id(base_manager_mock, param, expected_result):
    assert StudentManager.drop_student_by_id(param) == expected_result


def test_all_courses(base_manager_mock):
    for result in GropCourseManager.all_courses():
        assert result['name'] in COURSE_LIST


def test_pop_student_course(base_manager_mock):
    result = StudentManager.pop_student_course(
        first_name='Student_first',
        last_name='Student_last',
        id_group='3',
        id_course='2'
    )
    assert result['first_name'] == 'Student_first'


def test_new_course(base_manager_mock):
    result = GropCourseManager.new_course(
        course_name='Name cour',
        description='Cour desc'
    )
    assert result == {'id': 4, 'name': 'Name cour', 'description': 'Cour desc'}


@pytest.mark.parametrize('param, expected_result',
                         [('3', '3'),
                          ('3000', None)])
def test_delete_course(base_manager_mock, param, expected_result):
    result = CourseManager.delete_course(id_course=param)
    assert result == expected_result


@pytest.mark.parametrize('param,  expected_result',
                         [('2', {'description': 'This course is Flask',
                                 'id': 2, 'name': 'Flask'}),
                          ('3000', None)])
def test_get_by_id_course(base_manager_mock, param, expected_result):
    result = CourseManager.get_by_id_course(id_course=param)
    assert result == expected_result


@pytest.mark.parametrize('param, param1, param_id, expected_result',
                         [('Python', 'This course is Python', '1', {'description': 'This course is Python',
                                                                    'id': 1, 'name': 'Python'}),
                          ('3000', '3', '223', None)])
def test_update_name_course(base_manager_mock, param, param1, param_id, expected_result):
    result = CourseManager.update_name_course(id_course=param_id,
                                              course_name=param,
                                              description=param1)
    assert result == expected_result


@pytest.mark.parametrize('param, param1, expected_result',
                         [('2', '1', 'web_courses.models.student_model.StudentModel'),
                          ('3000', '1', 'None')])
def test_remove_student_course(base_manager_mock, param, param1, expected_result):
    result = StudentCourseManager.remove_student_course(course_id=param, student_id=param1)
    assert expected_result in str(result)


@pytest.mark.parametrize('param, expected_result',
                         [('2', "{'student_id': 1, 'course_id': 2}"),
                          ('3000', 'None')])
def test_get_students_in_course(base_manager_mock, param, expected_result):
    result = StudentCourseManager.get_students_in_course(id_course=param)
    assert expected_result in str(result)


@pytest.mark.parametrize('param, param1, expected_result',
                         [('2', '1', "{'id': '1', 'first_name': 'Billy', 'last_name': 'Garcia', 'id_group': 1}"),
                          ('2', '1000', 'None')])
def test_add_student_course(base_manager_mock, param, param1, expected_result):
    result = StudentCourseManager.add_student_course(id_course=param, id_student=param1)
    assert expected_result in str(result)
