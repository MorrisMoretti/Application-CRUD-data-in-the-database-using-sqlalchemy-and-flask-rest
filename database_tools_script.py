import argparse

from app import app
from constants import COURSE_LIST
from web_courses import PopulateDB
from web_courses.utils import DataGenerator


def run_parser() -> argparse.Namespace:
    """Run parser with arguments"""
    parser = argparse.ArgumentParser(description="Create db")
    parser.add_argument('--init_db', dest="init_db", action='store_true', default=None, help="Create tables")
    parser.add_argument('--pop_db', dest="pop_db", action='store_true', default=None, help="Pop db with random data")
    arg = parser.parse_args()
    if not any([arg.init_db, arg.pop_db]):
        raise ValueError('Please select --init_db, --pop_db')
    return arg


def main() -> None:
    args = run_parser()
    with app.app_context():
        if args.init_db:
            PopulateDB.create_tables()
        if args.pop_db:
            courses = PopulateDB.pop_course(course_list=COURSE_LIST)
            PopulateDB.pop_groups(groups=DataGenerator.groups())
            PopulateDB.pop_students(students=DataGenerator.students(), courses=courses)


if __name__ == '__main__':
    main()
