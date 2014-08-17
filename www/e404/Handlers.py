import www.base.BaseHandler
import logging

def render(response, template, **kw):
	t = www.base.BaseHandler.jinja_env.get_template(template)
	page = t.render(**kw)
	response.out.write(page)

def handle404(request, response, exception):
	# Unauthorized
	logging.exception(exception)
	render(response, "e404/e404.html")
	response.set_status(404)

class Error404Handler(www.base.BaseHandler.BaseHandler):
	def get(self):
		return self.abort(404)
