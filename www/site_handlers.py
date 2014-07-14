from webapp2_extras.routes import RedirectRoute

import www.index.handler

site_handlers = [
    RedirectRoute('/', handler=www.index.handler.default, name='Index', strict_slash=True)
]