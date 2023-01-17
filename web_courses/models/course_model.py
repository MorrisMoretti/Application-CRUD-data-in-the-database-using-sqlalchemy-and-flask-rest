from sqlalchemy import Column, Integer, String

from .base_model import Base


class CourseModel(Base):
    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
