import random
from dataclasses import dataclass
from string import ascii_uppercase
from typing import List

from names import get_first_name, get_last_name

from constants import COURSE_LIST
from web_courses.logger import get_logger

logging = get_logger(__name__)


@dataclass
class NewStudent:
    name: str
    last_name: str
    id_group: int
    course: str


class DataGenerator:

    @staticmethod
    def groups() -> List[str]:
        groups = [f"{''.join(random.choices(ascii_uppercase, k=2))}-{random.randint(10, 99)}" for _ in range(10)]
        return groups

    @staticmethod
    def students() -> List[NewStudent]:

        last_names = [get_last_name() for _ in range(20)]
        logging.info(f'Generate last_names: {len(last_names)}')

        names = [get_first_name() for _ in range(20)]
        logging.info(f'Generate names: {len(names)}')

        id_groups = [random.randint(1, 10) for _ in range(200)]
        logging.info(f'Generate id_groups: {len(id_groups)}')

        students = [NewStudent(name=random.choice(names),
                               last_name=random.choice(last_names),
                               id_group=id_group,
                               course=random.choice(COURSE_LIST)) for id_group in id_groups]
        return students
