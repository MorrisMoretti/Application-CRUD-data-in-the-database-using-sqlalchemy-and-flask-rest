from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import Base


class StudentModel(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    id_group = Column(Integer, ForeignKey('Groups.id'))
    course: Any = relationship(
        'CourseModel',
        secondary='association_table',
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "id_group": self.id_group,
        }
