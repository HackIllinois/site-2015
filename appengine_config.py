import sys
import os

# Include third party libraries
third_party = os.path.join(os.path.dirname(__file__), 'third_party')
sys.path.append(third_party)

# Include tropo so we can just import tropo
sys.path.append(os.path.join(third_party, 'tropo-webapi-python'))

# Include cloudstorage for resume upload
sys.path.append(os.path.join(third_party, 'cloudstorage'))

# Include requests for ease-of-use while integrating with SendGrid
sys.path.append(os.path.join(third_party, 'requests'))

# Include twilio
sys.path.append(os.path.join(third_party, 'twilio'))

# Include sources for google drive api
# Reference: https://developers.google.com/api-client-library/python/start/installation#appengine
#            https://developers.google.com/drive/web/quickstart/quickstart-python#step_2_install_the_google_client_library
# sys.path.append(os.path.join(third_party, 'apiclient'))
# sys.path.append(os.path.join(third_party, 'httplib2'))
# sys.path.append(os.path.join(third_party, 'oauth2client'))
# sys.path.append(os.path.join(third_party, 'uritemplate'))


# https://developers.google.com/appengine/docs/python/tools/appstats?csw=1
appstats_CALC_RPC_COSTS = True

def webapp_add_wsgi_middleware(app):
      from google.appengine.ext.appstats import recording
      app = recording.appstats_wsgi_middleware(app)
      return app
