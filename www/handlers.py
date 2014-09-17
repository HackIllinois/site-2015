from webapp2_extras.routes import RedirectRoute, DomainRoute

import www.index.Handlers
import www.error.Handlers

site_handlers = [
    RedirectRoute('/', handler=www.index.Handlers.MainHandler, name='Index', strict_slash=True),
    RedirectRoute('/404', handler=www.error.Handlers.Error404Handler, name='Error404', strict_slash=True),
]

error_handlers = {
    401: www.error.Handlers.handle401,
    404: www.error.Handlers.handle404,
}