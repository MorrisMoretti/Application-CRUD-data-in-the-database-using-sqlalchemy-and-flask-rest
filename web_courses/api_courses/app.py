from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from .api_views import (AllCoursesApi, AllStudentsApi, CountStudentsApi,
                        ManageCoursesApi, ManageStudentCoursesApi, StudentApi)

app = Flask(__name__)
api = Api(app)
Swagger(app)
API_URL = '/api/v1'

api.add_resource(CountStudentsApi, f'{API_URL}/groups/')
api.add_resource(AllStudentsApi, f'{API_URL}/students/')
api.add_resource(StudentApi, f'{API_URL}/students/student_id=<student_id>')
api.add_resource(AllCoursesApi, f'{API_URL}/courses/')
api.add_resource(ManageCoursesApi, f'{API_URL}/courses/course_id=<course_id>')
api.add_resource(ManageStudentCoursesApi, f'{API_URL}/student_course/course_id=<course_id>')
