import www.base.BaseHandler
import logging
from google.appengine.api import users

def render(response, template, **kw):
	t = www.base.BaseHandler.jinja_env.get_template(template)
	page = t.render(**kw)
	response.out.write(page)

def handle401(request, response, exception):
	# Unauthorized
	logging.exception(exception)
	url = users.create_logout_url('/')
	render(response, "error/e401.html", message="<a href='" + url + "'>Logout</a>")
	response.set_status(401)
	
def handle404(request, response, exception):
	# Unauthorized
	logging.exception(exception)
	render(response, "error/e404.html")
	response.set_status(404)

class Error401Handler(www.base.BaseHandler.BaseHandler):
	def get(self):
		return self.abort(401)

class Error404Handler(www.base.BaseHandler.BaseHandler):
	def get(self):
		return self.abort(404)
