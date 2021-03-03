"""
Module with class-based views for the framework.
"""
from datetime import datetime

from core.templator import render_template
from core.wsgi_core import Application
from logs.config import Logger
from models import OnlineUniversity
from core.decorators import UrlPaths, debug

site = OnlineUniversity()
logger = Logger('main')
routes = UrlPaths()


@routes.add_route('/')
class IndexView:
    """
    Class-based view for an index page
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML-code
        """
        logger.logger(f'{__name__}.py; IndexView; requested index page.')
        keyword = request.get('keyword', None)
        return '200 Ok', [render_template('templates/index.html',
                                          keyword=keyword).encode('utf-8')]


@routes.add_route('/all_courses/')
class CoursesListView:
    """
    Class-based view for a list of all available courses.
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML-code
        """
        logger.logger(
            f'{__name__}.py; CoursesListView; requested the list of courses.')
        return '200 Ok', [render_template(
            'templates/courses_list.html',
            objects_list=site.courses).encode('utf-8')]


@routes.add_route('/create_course/')
class CreateCourseView:
    """
    Class-based view for the course creation page.
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that handles the requests.
        If it's POST request the method extracts the data from
        the request and saves new course.
        In case of GET request the method simply renders the
        template with the list of course categories available.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        logger.logger(
            f'{__name__}.py: CreateCourseView; requested course creation.')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = Application.decode_value(name)
            cat_id = data.get('category_id')
            category = None
            if cat_id:
                category = site.find_category(int(cat_id))
                new_course = site.create_course('online', name, category)
                site.courses.append(new_course)
            return '200 Ok', [render_template(
                'templates/create_course.html').encode('utf-8')]
        else:
            categories = site.course_categories
            return '200 Ok', [render_template(
                'templates/create_course.html',
                categories=categories).encode('utf-8')]


@routes.add_route('/copy_course/')
class CopyCourseView:
    """
    Class-based view to handle the copying of a course.
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method. Handles the copying of a given
        course by invoking a Prototype Mixin method 'clone'.

        :param request: HTTP-requests
        :return: tuple, first element is string, second HTML code
        """
        params = request['request_params']
        name = params['name']
        logger.logger(
            f'{__name__}.py; CopyCourseView; copying course {name}.')
        old_course = site.get_course(name)
        if old_course:
            new_name = f'{name}_copy'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)
        return '200 Ok', [render_template(
            'templates/course_list.html',
            objects_list=site.courses).encode('utf-8')]


@routes.add_route('/all_categories/')
class CategoryListView:
    """
    Class-based view for the list of existing course categories.
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML-code
        """
        logger.logger(
            f'{__name__}.py; CategoryListView; '
            f'requested the list of course categories.')
        return '200 Ok', [render_template(
            'templates/categories_list.html',
            objects_list=site.course_categories).encode('utf-8')]


@routes.add_route('/create_category/')
class CreateCategoryView:
    """
    Class-based view for a category creation page.
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that handles the requests.
        If it's POST request the method extracts the data from
        the request and saves new category.
        In case of GET request the method simply renders the
        template with the list of course categories available.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        logger.logger(
            f'{__name__}.py; CreateCategoryView; creating new category.')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = Application.decode_value(name)
            cat_id = data.get('category_id')
            category = None
            if cat_id:
                category = site.find_category(int(cat_id))
            new_category = site.create_category(name, category)
            site.course_categories.append(new_category)
            return '200 Ok', [render_template(
                'templates/create_category.html').encode('utf-8')]
        else:
            categories = site.course_categories
            return '200 Ok', [render_template(
                'templates/create_category.html',
                categories=categories).encode('utf-8')]


@routes.add_route('/about/')
class AboutView:
    """
    Class-based view for an about page.
    """

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        logger.logger(f'{__name__}.py; AboutView; requested about page.')
        return '200 Ok', [render_template(
            'templates/about.html').encode('utf-8')]


@routes.add_route('/contacts/')
class ContactsView:
    """
    Class-based view for a contacts page.
    """

    @staticmethod
    @debug
    def save_to_file(request: dict) -> None:
        """
        Saves data from incoming POST-request to file.

        :param request: incoming data
        """
        try:
            logger.logger('Trying to save the POST-data to file.')
            with open(f"incoming_msg_{datetime.now()}.txt", 'w') as f:
                text = f"Incoming message:\n" \
                       f"From: {request['data']['email']};\n" \
                       f"Subject: {request['data']['header']};\n" \
                       f"Text:\n{request['data']['message']}"
                f.write(text)
                f.close()
        except Exception as e:
            logger.logger(f'Saving to file failed: {e}.')
        else:
            logger.logger('Data saved successfully.')

    @debug
    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second HTML code
        """
        logger.logger(f'{__name__}.py; ContactsView; requested Contacts page.')
        if request['method'] == 'POST':
            self.save_to_file(request)
            return '200 Ok', [render_template(
                'templates/contacts.html').encode('utf-8')]
        else:
            return '200 Ok', [render_template(
                'templates/contacts.html').encode('utf-8')]
