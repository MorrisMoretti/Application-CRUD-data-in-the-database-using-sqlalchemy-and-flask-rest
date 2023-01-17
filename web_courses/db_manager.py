import random
from typing import List

from database import engine_db, session_db

from .logger import get_logger
from .models import Base, CourseModel, GroupModel, StudentModel
from .utils import NewStudent

logging = get_logger(__name__)


class PopulateDB:
    session = session_db()
    data_base = engine_db

    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(cls.data_base)
        logging.info(f'Create new tables {list(Base.metadata.tables.keys())}')

    @classmethod
    def pop_groups(cls, groups: List[str]):
        new_groups = [cls.session.add(GroupModel(name=group)) for group in groups]
        cls.session.commit()
        logging.info(f'Add {len(new_groups)} groups in table')

    @classmethod
    def pop_course(cls, course_list: List) -> List[CourseModel]:
        insert_data = [CourseModel(name=course,
                                   description=f'This course is {course}') for course in course_list]
        cls.session.add_all(insert_data)

        cls.session.commit()
        logging.info(f'Add {len(cls.session.query(CourseModel).all())} courses in table')
        return cls.session.query(CourseModel).all()

    @classmethod
    def pop_students(cls, students: List[NewStudent], courses: List[CourseModel]):
        for student in students:
            new_student = StudentModel(first_name=student.name, last_name=student.last_name, id_group=student.id_group)
            new_student.course.append(random.choice(courses))
            cls.session.add(new_student)
        cls.session.commit()
        logging.info(f'Add {len(cls.session.query(StudentModel).all())} students in table')
