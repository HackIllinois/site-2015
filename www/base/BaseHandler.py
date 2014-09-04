import logging
import os
import jinja2
import webapp2

from google.appengine.ext import ereporter

from google.appengine.api import users

from db import constants

template_dir = os.path.join(os.path.dirname(__file__), os.pardir)
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
jinja_env.filters.update({'is_list':lambda l: isinstance(l, list)})

#https://developers.google.com/appengine/articles/python/recording_exceptions_with_ereporter
ereporter.register_logger()


class BaseHandler(webapp2.RequestHandler):
    """ This is the Base Handler
        This is the parent of every other handler
        Most other handlers use functions defined in this hander
        This handler is the child of webapp2.RequestHandler which is pre-defined by webapp2"""

    def __init__(self, request, response):
        super(BaseHandler, self).__init__(request, response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        page = t.render(params)

        return page
