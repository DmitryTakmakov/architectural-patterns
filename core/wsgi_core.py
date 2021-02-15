"""
The core module of the WSGI framework.
"""
import re

from views import NotFoundView


class Application:
    """
    The core class of the WSGI framework.
    Takes in the dict with url-patterns and the list of
    front-controllers and then checks for what HTML-page to show
    based on the path.
    """

    def __init__(self, urls: dict, fronts: list):
        """
        :param urls: url paths
        :param fronts: front controllers
        """
        self.urls = urls
        self.front_controllers = fronts
        self.request = {}

    def __call__(self, environment: dict, start_response) -> list:
        """

        :param environment:
        :param start_response:
        :return:
        """
        path = environment['PATH_INFO']
        if re.findall(r'\w+\/$', path):
            path = path[:-1]
        print(path)
        if path in self.urls:
            view = self.urls[path]
            for controller in self.front_controllers:
                controller(self.request)
        else:
            view = NotFoundView()
        resp, body = view(self.request)
        start_response(resp, [('Content-Type', 'text/html')])
        return body
