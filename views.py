"""
Module with class-based views for the framework.
"""
from datetime import datetime

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


class ContactsView:
    """
    Class-based view for a contacts page.
    """

    def save_to_file(self, request: dict) -> None:
        """
        Saves data from incoming POST-request to file.

        :param request: incoming data
        """
        with open(f"incoming_msg_{datetime.now()}", 'w') as f:
            text = f"Incoming message:\n" \
                   f"From: {request['data']['email']};\n" \
                   f"Subject: {request['data']['header']};\n" \
                   f"Text:\n{request['data']['message']}"
            f.write(text)
            f.close()

    def __call__(self, request: dict) -> tuple:
        """
        Main callable method that does the magic.

        :param request: HTTP-request
        :return: tuple, first element is string, second - HTML-code
        """
        if request['method'] == 'POST':
            self.save_to_file(request)
            return '200 Ok', [render_template(
                'templates/contacts.html').encode('utf-8')]
        else:
            return '200 Ok', [render_template(
                'templates/contacts.html').encode('utf-8')]


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
