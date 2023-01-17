import json
from http import HTTPStatus

from tests.conftest import ALL_STUD, COUNT_ST, COURSES

API_URL = '/api/v1'


def test_count_students_api_get(group_course_manager_mock, client):
    group_course_manager_mock.group_count_students.return_value = COUNT_ST
    response = client.get(f'{API_URL}{"/groups/"}')
    assert COUNT_ST == response.json
    assert response.status_code == HTTPStatus.OK
    group_course_manager_mock.group_count_students.assert_called()


def test_all_students_api_get(student_manager_mock, client):
    student_manager_mock.all_students.return_value = ALL_STUD
    response = client.get(f'{API_URL}{"/students/"}')
    assert ALL_STUD == response.json
    assert response.status_code == HTTPStatus.OK
    student_manager_mock.all_students.assert_called()


def test_all_students_api_post(student_manager_mock, client):
    student_manager_mock.pop_student_course.return_value = next(iter(ALL_STUD))
    response = client.post(f'{API_URL}{"/students/"}', data=json.dumps(dict(first_name='NewName',
                                                                            last_name='NewDesk',
                                                                            id_group=2,
                                                                            id_course=2)),
                           content_type='application/json')
    assert next(iter(ALL_STUD)) == response.json
    assert response.status_code == HTTPStatus.CREATED
    student_manager_mock.pop_student_course.assert_called()


def test_all_students_api_post_fail(student_manager_mock, client):
    student_manager_mock.pop_student_course.return_value = None
    response = client.post(f'{API_URL}{"/students/"}', data=json.dumps(dict(first_name='NewName',
                                                                            last_name='NewDesk',
                                                                            id_group=2,
                                                                            id_course=2)),
                           content_type='application/json')
    assert {'error': 'Course or group not found.'} == response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    student_manager_mock.pop_student_course.assert_called()


def test_student_api_get(student_manager_mock, client):
    student_manager_mock.find_student_by_id.return_value = next(iter(ALL_STUD))
    response = client.get(f'{API_URL}{"/students/student_id=1"}')
    assert next(iter(ALL_STUD)) == response.json
    assert response.status_code == HTTPStatus.OK
    student_manager_mock.find_student_by_id.assert_called()


def test_student_api_get_fail(student_manager_mock, client):
    student_manager_mock.find_student_by_id.return_value = None
    response = client.get(f'{API_URL}{"/students/student_id=1"}')
    assert {'error': 'Student not found.'} == response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    student_manager_mock.find_student_by_id.assert_called()


def test_student_api_delete(student_manager_mock, client):
    student_manager_mock.drop_student_by_id.return_value = next(iter(ALL_STUD))
    response = client.delete(f'{API_URL}{"/students/student_id=1"}')
    assert HTTPStatus.NO_CONTENT == response.status_code
    student_manager_mock.drop_student_by_id.assert_called()


def test_student_api_delete_fail(student_manager_mock, client):
    student_manager_mock.drop_student_by_id.return_value = None
    response = client.delete(f'{API_URL}{"/students/student_id=1"}')
    assert HTTPStatus.NOT_FOUND == response.status_code
    student_manager_mock.drop_student_by_id.assert_called()


def test_all_courses_api_get(group_course_manager_mock, client):
    group_course_manager_mock.all_courses.return_value = COURSES
    response = client.get(f'{API_URL}{"/courses/"}')
    assert COURSES == response.json
    assert response.status_code == HTTPStatus.OK
    group_course_manager_mock.all_courses.assert_called()


def test_all_courses_api_post(group_course_manager_mock, client):
    group_course_manager_mock.new_course.return_value = next(iter(COURSES))
    response = client.post(f'{API_URL}{"/courses/"}', data=json.dumps(dict(
        course_name='Flask',
        description='Desk')), content_type='application/json')
    assert next(iter(COURSES)) == response.json
    assert response.status_code == HTTPStatus.CREATED
    group_course_manager_mock.new_course.assert_called()


def test_manage_courses_api_get(course_manager_mock, client):
    course_manager_mock.get_by_id_course.return_value = next(iter(COURSES))
    response = client.get(f'{API_URL}{"/courses/course_id=1"}')
    assert next(iter(COURSES)) == response.json
    assert response.status_code == HTTPStatus.OK
    course_manager_mock.get_by_id_course.assert_called()


def test_manage_courses_api_get_fail(course_manager_mock, client):
    course_manager_mock.get_by_id_course.return_value = None
    response = client.get(f'{API_URL}{"/courses/course_id=1"}')
    assert {'error': 'Course not found.'} == response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    course_manager_mock.get_by_id_course.assert_called()


def test_manage_courses_api_del(course_manager_mock, client):
    course_manager_mock.delete_course.return_value = '1'
    response = client.delete(f'{API_URL}{"/courses/course_id=1"}')
    assert HTTPStatus.NO_CONTENT == response.status_code
    course_manager_mock.delete_course.assert_called()


def test_manage_courses_api_del_fail(course_manager_mock, client):
    course_manager_mock.delete_course.return_value = None
    response = client.delete(f'{API_URL}{"/courses/course_id=1"}')
    assert HTTPStatus.NOT_FOUND == response.status_code
    course_manager_mock.delete_course.assert_called()


def test_manage_courses_api_put(course_manager_mock, client):
    course_manager_mock.update_name_course.return_value = next(iter(COURSES))
    response = client.put(f'{API_URL}{"/courses/course_id=2"}', data=json.dumps(dict(id=2,
                                                                                     course_name='NewName',
                                                                                     description='NewDesk')),
                          content_type='application/json')
    assert next(iter(COURSES)) == response.json
    assert response.status_code == HTTPStatus.OK
    course_manager_mock.update_name_course.assert_called()


def test_manage_courses_api_put_fail(course_manager_mock, client):
    course_manager_mock.update_name_course.return_value = None
    response = client.put(f'{API_URL}{"/courses/course_id=2"}', data=json.dumps(dict(id=2,
                                                                                     course_name='NewName',
                                                                                     description='NewDesk')),
                          content_type='application/json')
    assert {'error': 'Course not found.'} == response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    course_manager_mock.update_name_course.assert_called()


def test_manage_student_courses_api_delete(student_course_manager_mock, client):
    student_course_manager_mock.remove_student_course.return_value = 'Successful remove student'
    response = client.delete(f'{API_URL}{"/student_course/course_id=9"}', data=json.dumps(dict(student_id=2)),
                             content_type='application/json')
    assert HTTPStatus.NO_CONTENT == response.status_code
    student_course_manager_mock.remove_student_course.assert_called()


def test_manage_student_courses_api_delete_fail(student_course_manager_mock, client):
    student_course_manager_mock.remove_student_course.return_value = None
    response = client.delete(f'{API_URL}{"/student_course/course_id=9"}', data=json.dumps(dict(student_id=2)),
                             content_type='application/json')
    assert HTTPStatus.NOT_FOUND == response.status_code
    student_course_manager_mock.remove_student_course.assert_called()


def test_manage_student_courses_api_get(student_course_manager_mock, client):
    student_course_manager_mock.get_students_in_course.return_value = next(iter(COURSES))
    response = client.get(f'{API_URL}{"/student_course/course_id=9"}')
    assert next(iter(COURSES)) == response.json
    assert response.status_code == HTTPStatus.OK
    student_course_manager_mock.get_students_in_course.assert_called()


def test_manage_student_courses_api_get_fail(student_course_manager_mock, client):
    student_course_manager_mock.get_students_in_course.return_value = None
    response = client.get(f'{API_URL}{"/student_course/course_id=9"}')
    assert {'error': 'Course not found.'} == response.json
    student_course_manager_mock.get_students_in_course.assert_called()


def test_manage_student_courses_api_post(student_course_manager_mock, client):
    student_course_manager_mock.add_student_course.return_value = next(iter(ALL_STUD))
    response = client.post(f'{API_URL}{"/student_course/course_id=9"}',
                           data=json.dumps(dict(course_id=2, student_id=2)),
                           content_type='application/json')
    assert next(iter(ALL_STUD)) == response.json
    assert response.status_code == HTTPStatus.CREATED
    student_course_manager_mock.add_student_course.assert_called()


def test_manage_student_courses_api_post_fail(student_course_manager_mock, client):
    student_course_manager_mock.add_student_course.return_value = None
    response = client.post(f'{API_URL}{"/student_course/course_id=9"}',
                           data=json.dumps(dict(course_id=2, student_id=2)),
                           content_type='application/json')
    assert {'error': 'Student or course id not found.'} == response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    student_course_manager_mock.add_student_course.assert_called()
