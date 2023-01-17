from sqlalchemy import Column, ForeignKey

from .base_model import Base


class Association(Base):
    __tablename__ = "association_table"

    student_id = Column(ForeignKey('Students.id', ondelete="CASCADE"), primary_key=True)
    course_id = Column(ForeignKey('Courses.id', ondelete="CASCADE"), primary_key=True)

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "course_id": self.course_id
        }
