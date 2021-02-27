"""
Module containing models for future use with the ORM and classes
(e.g. factories) used by the main OnlineUniversity class.
"""
from core.bases import User, Factory, PrototypeMixin


class Student(User):
    """
    Class representing students in the ORM.
    """


class Teacher(User):
    """
    Class representing teachers in the ORM.
    """


class UserFactory(Factory):
    """
    Factory class used for creation of the users.
    user_types is a dictionary that stores information about
    all available user types.
    """
    user_types = {
        'teacher': Teacher,
        'student': Student
    }

    @classmethod
    def create(cls, type_: str) -> User:
        """
        Creates the users of the given type.

        :param type_: the type of the user in string format
        :return: a new instance of the given class
        """
        return cls.user_types[type_]()


class CourseCategory:
    """
    Class representing the categories of the courses in the ORM.
    """
    auto_id = 0

    def __init__(self, name: str, category):
        """
        Initializes the course category, increases the auto_id by 1.

        :param name: category name
        :param category: can be either a CourseCategory object or None
        """
        self.id = CourseCategory.auto_id
        CourseCategory.auto_id += 1
        self.name = name
        self.category = category
        self.existing_courses = []

    def count_courses(self) -> int:
        """
        Counts the number of existing courses and returns the value.

        :return: the number of existing courses.
        """
        res = len(self.existing_courses)
        if self.category:
            res += self.category.count_courses()
        return res


class Course(PrototypeMixin):
    """
    Main abstract class for courses, inherits from the Prototype Mixin
    which allows for cloning of existing courses.
    """

    def __init__(self, course_name: str, course_category: CourseCategory):
        """
        Initializes the Course object and appends it to the list of
        existing courses.

        :param course_name:
        :param course_category:
        """
        self.name = course_name
        self.category = course_category
        self.category.existing_courses.append(self)


class OnlineCourse(Course):
    """
    Class representing the online courses in the ORM.
    """


class OfflineCourse(Course):
    """
    Class representing the offline courses in the ORM.
    """


class WebinarCourse(Course):
    """
    Class representing the webinars in the ORM.
    """


class CourseFactory(Factory):
    """
    Factory class used for creation of the courses.
    course_types is a dictionary that stores information about all
    available course types.
    """
    course_types = {
        'online': OnlineCourse,
        'offline': OfflineCourse,
        'webinar': WebinarCourse
    }

    @classmethod
    def create(
            cls, type_: str, name: str, category: CourseCategory) -> Course:
        """
        Creates the course of the given type with the given name under
        the given category.

        :param type_: type of the course
        :param name: name of the course
        :param category: course category
        :return: an instance of the given Course subclass
        """
        return cls.course_types[type_](name, category)


class OnlineUniversity:
    """
    The main class of the online university, built with this simple
    WSGI framework.
    """

    def __init__(self):
        """
        Initializes the main class.
        Creates the necessary data structures.
        """
        self.teachers = []
        self.students = []
        self.course_categories = []
        self.courses = []

    @staticmethod
    def create_user(type_: str) -> User:
        """
        Creates the user with the help of the user factory.

        :param type_: string with the user type,
        can be either student or teacher

        :return: an instance of one of the User subclasses
        """
        return UserFactory.create(type_)

    @staticmethod
    def create_category(
            name: str, category: CourseCategory = None) -> CourseCategory:
        """
        Creates a course category with the given name. Can also
        take the already existing category, but that is not mandatory.

        :param name: category name
        :param category: existing category
        :return: an instance of the CourseCategory class
        """
        return CourseCategory(name, category)

    def find_category(self, cat_id: int) -> CourseCategory:
        """
        Looks for an existing category by its ID.
        If nothing found raises an exception.

        :param cat_id: category ID
        :return: an instance of CourseCategory class
        """
        for item in self.course_categories:
            if item.id == cat_id:
                return item
        raise Exception(f"There's no category with id {cat_id}")

    @staticmethod
    def create_course(type_, name, category) -> Course:
        """
        Creates a course of the given type, with the given name and
        under the given category.

        :param type_: the type of the course
        :param name: the name of the course
        :param category: the category of the course
        :return: an instance of one of Course subclasses
        """
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> (Course, None):
        """
        Tries to fetch a course by name. If nothing has been found
        returns None instead.

        :param name: name of the course in string format
        :return: either an instance of one of Course subclasses or None
        """
        for item in self.courses:
            if item.name == name:
                return item
        return None
