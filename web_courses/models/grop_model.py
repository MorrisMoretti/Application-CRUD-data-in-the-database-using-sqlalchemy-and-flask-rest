from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base_model import Base


class GroupModel(Base):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_group = relationship('StudentModel')

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }
