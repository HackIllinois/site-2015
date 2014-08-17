from webapp2_extras.routes import RedirectRoute

import www.index.Handlers
import www.e401.Handlers
import www.e404.Handlers
import www.base.LogoutHandler

site_handlers = [
    RedirectRoute('/', handler=www.index.Handlers.MainHandler, name='Index', strict_slash=True),
    RedirectRoute('/logout', handler=www.base.LogoutHandler.LogoutHandler, name='Logout', strict_slash=True),
    RedirectRoute('/404', handler=www.e404.Handlers.Error404Handler, name='Error404', strict_slash=True),
]

error_handlers = {
    401: www.e401.Handlers.handle401,
    404: www.e404.Handlers.handle404,
}