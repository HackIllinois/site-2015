from webapp2_extras.routes import RedirectRoute, DomainRoute

import www.index.handlers
import www.error.handlers
import www.admin.handlers

www_handlers = [
    RedirectRoute('/', handler=www.index.handlers.MainHandler, name='Index', strict_slash=True),
    RedirectRoute('/404', handler=www.error.handlers.Error404Handler, name='Error404', strict_slash=True),

    # Admin routes
    RedirectRoute('/admin', handler=www.admin.handlers.AdminHomeHandler, name='AdminHome', strict_slash=True),
]

error_handlers = {
    404: www.error.handlers.handle404,
}
