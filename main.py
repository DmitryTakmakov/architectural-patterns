"""
Main module of the framework. Defines front controllers, url-patterns
and calls the core app.
"""
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
