import sys
import os

# https://developers.google.com/appengine/docs/python/tools/appstats?csw=1
appstats_CALC_RPC_COSTS = True

def webapp_add_wsgi_middleware(app):
      from google.appengine.ext.appstats import recording
      app = recording.appstats_wsgi_middleware(app)
      return app
