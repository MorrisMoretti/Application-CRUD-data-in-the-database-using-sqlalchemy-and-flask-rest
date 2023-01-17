from flask import Response, jsonify, make_response, request
from flask_restful import Resource

from .courses_manager import (CourseManager, GropCourseManager,
                              StudentCourseManager, StudentManager)


class CountStudentsApi(Resource):

    def get(self) -> Response:
        """
        Count students in Groups
        ---
        tags:
            - Count students in Groups
        responses:
          200:
            description: Count students in Groups
            schema:
              type: "objects"
              properties:
                order:
                  type: "objects"
              example: {"id": 10, "name": "CP-33", "students": 16}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        grop_count = GropCourseManager.group_count_students()
        return jsonify(grop_count)


class AllStudentsApi(Resource):

    def get(self) -> Response:
        """
        Get all students
        ---
        tags:
            -  Get all/add students
        responses:
          200:
            description: All students
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id": "1", "first_name": "Richard", "last_name": "Durazo", "id_group": 1}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        all_stud = StudentManager.all_students()
        return jsonify(all_stud)

    def post(self) -> Response:
        """
        Add new student
        ---
        tags:
            -  Get all/add students
        post:
            summary: Creates a new student.
            consumes:
                - application/json
        parameters:
          - in: body
            name: NewStudent
            schema:
                type: object
                description: The student to create.
                properties:
                  first_name:
                    example: 'First_name'
                    type: string
                  last_name:
                    example: 'Last_name'
                    type: string
                  id_group:
                    example: 1
                    type: integer
                  id_course:
                    example: 1
                    type: integer
        responses:
          201:
            description: Add new student
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id": "205", "first_name": "Jon", "last_name": "Jones", "id_group": 2}
          404:
            description: Course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Course or group not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        id_group = request.json['id_group']
        id_course = request.json['id_course']
        stud_cour = StudentManager.pop_student_course(first_name=first_name,
                                                      last_name=last_name,
                                                      id_group=id_group,
                                                      id_course=id_course)
        if not stud_cour:
            return make_response({'error': 'Course or group not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return make_response(stud_cour, 201,
                             {'content-type': 'application/json; charset=utf-8'})


class StudentApi(Resource):

    def get(self, student_id: str) -> Response:
        """
        Get student by id
        ---
        tags:
            -  Get or dell student
        parameters:
          - name: 'student_id'
            default: 1
            in: path
            type: string
            required: true
        responses:
          200:
            description: Get student by id
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id": "4","first_name": "Lisa","last_name": "Thurber","id_group": 10,
                        "course":{"id_course": 3,"name": "Cli","description": "This course is Cli"}}
          404:
            description: Student not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Student not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        stud_by_id = StudentManager.find_student_by_id(student_id=student_id)
        if not stud_by_id:
            return make_response({'error': 'Student not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return jsonify(stud_by_id)

    def delete(self, student_id: str) -> Response:
        """
        Delete student by id
        ---
        tags:
            -  Get or dell student
        parameters:
          - name: 'student_id'
            default: 1
            in: path
            type: string
            required: true
        responses:
          204:
            description: Delete student by id
          404:
            description: Student not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Student not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        student_to_delete = StudentManager.drop_student_by_id(student_id=student_id)
        if not student_to_delete:
            return make_response({'error': 'Student not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return make_response('None', 204)


class AllCoursesApi(Resource):

    def get(self) -> Response:
        """
        Get all Courses
        ---
        tags:
            -  Get all/add Courses
        responses:
          200:
            description: Get all courses
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id": 1, "name": "Python", "description": "This course is Python"}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        courses = GropCourseManager.all_courses()
        return jsonify(courses)

    def post(self) -> Response:
        """
        Add new course
        ---
        tags:
            - Get all/add Courses
        post:
            summary: Creates a new course.
            consumes:
                - application/json
        parameters:
          - in: body
            name: NewCourse
            schema:
                type: object
                description: The course to create.
                properties:
                  course_name:
                    example: 'Flask_new'
                    type: string
                  description:
                    example: 'Flask new best course'
                    type: string
        responses:
          201:
            description: Add new course
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id": 2, "name": "Flask","description": "This course is Flask"}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        course_name = request.json['course_name']
        description = request.json['description']

        new_course = GropCourseManager.new_course(course_name=course_name,
                                                  description=description)
        return make_response(new_course, 201,
                             {'content-type': 'application/json; charset=utf-8'})


class ManageCoursesApi(Resource):

    def get(self, course_id: str) -> Response:
        """
        Get course by id
        ---
        tags:
            -  Manage course
        parameters:
          - name: 'course_id'
            default: 9
            in: path
            type: string
            required: true
        responses:
          200:
            description: Get course by id
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id_course": 2,"name": "New name","description": "New flask course"}
          404:
            description: Course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Course not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        get_course = CourseManager.get_by_id_course(id_course=course_id)
        if not get_course:
            return make_response({'error': 'Course not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return jsonify(get_course)

    def delete(self, course_id: str) -> Response:
        """
        Delete course by id
        ---
        tags:
            -  Manage course
        parameters:
          - name: 'course_id'
            default: 9
            in: path
            type: string
            required: true
        responses:
          204:
            description: Delete course by id
          404:
            description: Course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Course not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        delete_course = CourseManager.delete_course(id_course=course_id)
        if not delete_course:
            return make_response({'error': 'Course not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return make_response('None', 204)

    def put(self, course_id: str) -> Response:
        """
        Update course name and description by id
        ---
        tags:
            -  Manage course
        put:
            summary: Update course.
            consumes:
                - application/json
        parameters:
          - in: body
            name:  UpdateCourse
            schema:
                type: object
                description: The student to create.
                properties:
                  course_name:
                    example: 'NewName'
                    type: string
                  description:
                    example: 'New flask course'
                    type: string
          - name: 'course_id'
            default: 9
            in: path
            type: string
            required: true
        responses:
          200:
            description: Update course by id
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"id_course": 2,"name": "New name","description": "New flask course"}
          404:
            description: Course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Course not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        course_name = request.json['course_name']
        description = request.json['description']
        update_course = CourseManager.update_name_course(id_course=course_id,
                                                         course_name=course_name,
                                                         description=description)
        if not update_course:
            return make_response({'error': 'Course not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return jsonify(update_course)


class ManageStudentCoursesApi(Resource):

    def delete(self, course_id: str) -> Response:
        """
        Delete student for course by id
        ---
        tags:
            -  Manage student by course
        parameters:
          - in: body
            name: Student id
            schema:
                type: object
                description: Student id
                properties:
                  student_id:
                    example: 2
                    type: integer
          - name: 'course_id'
            default: 9
            in: path
            type: string
            required: true
        responses:
          204:
            description: Delete student for course by id
          404:
            description: Student or course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Student or course not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        student_id = request.json['student_id']
        new_course = StudentCourseManager.remove_student_course(course_id=course_id,
                                                                student_id=student_id)
        if not new_course:
            return make_response({'error': 'Student or course not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return make_response('None', 204)

    def get(self, course_id: str) -> Response:
        """
        Get all students by course id
        ---
        tags:
            -  Manage student by course
        parameters:
          - name: 'course_id'
            default: 9
            in: path
            type: string
            required: true
        responses:
          200:
            description: Get all students by course id
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: "{'student_id': 24, 'course_id': 9}"
          404:
            description: Course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Course not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        get_course = StudentCourseManager.get_students_in_course(id_course=course_id)
        if not get_course:
            return make_response({'error': 'Course not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return jsonify(get_course)

    def post(self, course_id: str) -> Response:
        """
        Add student to course by his id
        ---
        tags:
            -  Manage student by course
        post:
            summary: Add student to course
            consumes:
                - application/json
        parameters:

          - in: body
            name: NewStudent
            schema:
                type: object
                description: The student to create.
                properties:
                  student_id:
                    example: 88
                    type: integer
          - name: 'course_id'
            default: 9
            in: path
            type: string
            required: true
        responses:
          201:
            description: Add student to course
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: "Successful add student {'id': '8', 'first_name': 'Michael',
              'last_name': 'Francois', 'id_group': 2} to
              {'id_course': 6, 'name': 'HTML', 'description': 'This course is HTML'}"
          404:
            description: Course not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: {"error": "Student or course id not found."}
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        student_id = request.json['student_id']
        add_student_course = StudentCourseManager.add_student_course(id_course=course_id, id_student=student_id)
        if not add_student_course:
            return make_response({'error': 'Student or course id not found.'}, 404,
                                 {'content-type': 'application/json; charset=utf-8'})
        return make_response(jsonify(add_student_course), 201,
                             {'content-type': 'application/json; charset=utf-8'})
