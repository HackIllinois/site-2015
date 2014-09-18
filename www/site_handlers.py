from webapp2_extras.routes import RedirectRoute, DomainRoute

import www.index.handlers
import www.error.handlers

www_handlers = [
    RedirectRoute('/', handler=www.index.handlers.MainHandler, name='Index', strict_slash=True),
    RedirectRoute('/404', handler=www.error.handlers.Error404Handler, name='Error404', strict_slash=True),
]

error_handlers = {
    401: www.error.handlers.handle401,
    404: www.error.handlers.handle404,
}