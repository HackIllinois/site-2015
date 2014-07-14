import os
import jinja2
import webapp2
from google.appengine.ext import ereporter
import logging

template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
jinja_env.filters.update({'is_list':lambda l: isinstance(l, list)})

# https://developers.google.com/appengine/articles/python/recording_exceptions_with_ereporter
ereporter.register_logger()


class handler(webapp2.RequestHandler):
    """ Someone should fill in what this is """

    def __init__(self, request, response):
        super(handler, self).__init__(request, response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        page = t.render(params)

        return page