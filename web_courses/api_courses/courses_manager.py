from typing import Any, Dict, List, Optional

import sqlalchemy

from database import session_db
from web_courses.models import (Association, CourseModel, GroupModel,
                                StudentModel)


class BaseManager:
    session = session_db()


class GropCourseManager(BaseManager):

    @classmethod
    def group_count_students(cls) -> List[Dict[str, Any]]:
        count_stud_gr = cls.session.query(GroupModel, sqlalchemy.func.count(StudentModel.id_group)
                                          ).outerjoin(
            StudentModel, GroupModel.id == StudentModel.id_group
        ).group_by(
            GroupModel.id
        ).all()
        return [dict(**group.to_dict(), **{'students': numb_stud}) for group, numb_stud in count_stud_gr]

    @classmethod
    def all_courses(cls) -> List[Dict[str, Any]]:
        all_course = cls.session.query(CourseModel).all()
        return [course.to_dict() for course in all_course]

    @classmethod
    def new_course(cls, course_name: str, description: str) -> Dict[str, Any]:
        course = CourseModel(name=course_name, description=description)
        cls.session.add(course)
        cls.session.commit()
        return course.to_dict()


class StudentManager(BaseManager):

    @classmethod
    def find_student_by_id(cls, student_id: str) -> Dict[str, Any]:
        student_info = cls.session.query(
            StudentModel, CourseModel
        ).outerjoin(
            CourseModel, StudentModel.course
        ).filter(StudentModel.id == int(student_id)).all()
        if not student_info:
            return student_info
        student_dict = []
        courses = {}
        for student, course in student_info:
            student_dict = student.to_dict()
            if course:
                courses[course.name] = course.to_dict()
        return {**student_dict, 'course': courses}

    @classmethod
    def drop_student_by_id(cls, student_id: str) -> Optional[str]:
        student = cls.session.query(StudentModel).filter_by(id=student_id).first()
        if not student:
            return None
        cls.session.delete(student)
        cls.session.commit()
        return student_id

    @classmethod
    def pop_student_course(cls, **new_stud) -> Optional[dict]:
        new_student = StudentModel(
            first_name=new_stud['first_name'],
            last_name=new_stud['last_name'],
            id_group=new_stud['id_group']
        )
        course = cls.session.query(CourseModel).get(int(new_stud['id_course']))
        group = cls.session.query(GroupModel).filter_by(id=new_stud['id_group']).first()
        if not all([group, course]):
            return None
        new_student.course.append(course)
        cls.session.add(new_student)
        cls.session.commit()
        return new_student.to_dict()

    @classmethod
    def all_students(cls) -> List[Dict[str, Any]]:
        students = cls.session.query(StudentModel).all()
        return [student.to_dict() for student in students]


class CourseManager(BaseManager):

    @classmethod
    def delete_course(cls, id_course: str) -> Optional[str]:
        course = cls.session.query(CourseModel).filter_by(id=id_course).first()
        if not course:
            return None
        cls.session.delete(course)
        cls.session.commit()
        return id_course

    @classmethod
    def get_by_id_course(cls, id_course: str) -> Optional[List]:
        course = cls.session.query(CourseModel).filter_by(id=id_course).first()
        if not course:
            return None
        return course.to_dict()

    @classmethod
    def update_name_course(cls, id_course: str, course_name: str, description: str) -> Optional[List]:
        course = cls.session.query(CourseModel).get(id_course)
        if not course:
            return None
        course.name = course_name
        course.description = description
        cls.session.commit()
        return course.to_dict()


class StudentCourseManager(BaseManager):

    @classmethod
    def remove_student_course(cls, course_id: str, student_id: str) -> Optional[str]:
        student = cls.session.query(StudentModel).filter(StudentModel.id == student_id).first()
        course_a = cls.session.query(Association).filter_by(course_id=course_id,
                                                            student_id=student_id).first()
        course = cls.session.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not all([course, course_a]):
            return None
        student.course.remove(course)
        cls.session.commit()
        return student

    @classmethod
    def get_students_in_course(cls, id_course: str) -> Optional[List]:
        students = cls.session.query(Association).filter(Association.course_id == id_course).all()
        if not students:
            return None
        return [student.to_dict() for student in students]

    @classmethod
    def add_student_course(cls, id_course: str, id_student: str) -> Optional[Dict]:
        student = cls.session.query(StudentModel).filter_by(id=id_student).first()
        course = cls.session.query(CourseModel).filter(CourseModel.id == id_course).first()
        if not all([student, course]):
            return None
        student.course.append(course)
        cls.session.commit()
        return student.to_dict()
