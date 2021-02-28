"""
Main module of the framework. Defines front controllers, url-patterns
and calls the core app.
"""
from wsgiref.simple_server import make_server

from core.wsgi_core import Application
from views import IndexView, AboutView, ContactsView, CoursesListView, \
    CreateCourseView, CreateCategoryView, CopyCourseView, CategoryListView


def front_controller(request: dict):
    """
    A simple front controller that just changes one thing in context.
    For now!

    :param request: HTTP-request
    """
    request['keyword'] = 'ЖИЖНЯ!'


routes = {
    '/': IndexView(),
    '/about/': AboutView(),
    '/contacts/': ContactsView(),
    '/all_courses/': CoursesListView(),
    '/create_course/': CreateCourseView(),
    '/copy_course/': CopyCourseView(),
    '/all_categories/': CategoryListView(),
    '/create_category/': CreateCategoryView(),
}

controllers = [
    front_controller
]

application = Application(routes, controllers)

with make_server('127.0.0.1', 8000, application) as httpd:
    print('Running HTTP-server on port 8000...')
    httpd.serve_forever()
