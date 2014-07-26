from webapp2_extras.routes import RedirectRoute

import www.index.Handlers

site_handlers = [
    RedirectRoute('/', handler=www.index.Handlers.MainHandler, name='Index', strict_slash=True)
]
