from webapp2_extras.routes import RedirectRoute, DomainRoute

import www.index.handlers
import www.error.handlers
import www.admin.handlers
import www.base.handlers

www_handlers = [
    RedirectRoute('/', handler=www.index.handlers.IndexHandler, name='Index', strict_slash=True),
    RedirectRoute('/401', handler=www.error.handlers.Error401Handler, name='Error401', strict_slash=True),
    RedirectRoute('/404', handler=www.error.handlers.Error404Handler, name='Error404', strict_slash=True),
    RedirectRoute('/logout', handler=www.base.handlers.LogoutHandler, name='Logout', strict_slash=True),

    # Admin routes
    RedirectRoute('/admin', handler=www.admin.handlers.AdminHandler, name='Admin', strict_slash=True),
]

error_handlers = {
    401: www.error.handlers.handle401,
    404: www.error.handlers.handle404,
}
