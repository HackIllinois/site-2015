from www.base.BaseHandler import BaseHandler


class AdminHomeHandler(BaseHandler):
    """Homepage for the admin section."""

    def get(self):
        self.render('admin/default.html')
