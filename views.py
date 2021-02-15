"""
Module with class-based views for the framework.
"""
from core.templator import render_template


class IndexView:
    """
    Class-based view for an index page
    """

    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
        keyword = request.get('keyword', None)
        return '200 Ok', [render_template('templates/index.html',
                                          keyword=keyword).encode('utf-8')]


class AboutView:
    """
    Class-based view for an about page.
    """

    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
        return '200 Ok', [render_template(
            'templates/about.html').encode('utf-8')]


class NotFoundView:
    """
    Class-based view for a non-existent page.
    """

    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second - list with bytes
        """
        return '404 NOT FOUND', [b'Page not found!']
