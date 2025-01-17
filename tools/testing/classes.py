# fAppend the parent directory so modules in the parent directory can be imported
import os, sys

#You may need to change these paths
sys.path.append(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), os.path.pardir)))

import unittest, json, pickle, base64, webtest
from google.appengine.ext import testbed
from google.appengine.api import apiproxy_stub_map
from main import app

from google.appengine.tools import dev_appserver_index
from google.appengine.datastore import datastore_stub_util

#
# Datastore Test Class
#

class DatastoreTestCase(unittest.TestCase):
    def setUp(self):
        root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

        # Create the testbed and setup the testing environment. The testbed must be activated to work properly
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        
        #Use for testing eventual consistancy
        #self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        #self.policy.SetSeed(2) # Use the pseudo random sequence derived from seed=2.

        # Initialize the testbed stubs
        self.testbed.init_datastore_v3_stub(use_sqlite=True, root_path=root_directory, require_indexes=True)# consistency_policy=self.policy
        self.testbed.init_memcache_stub()

        # Create the index updater
        dev_appserver_index.SetupIndexes(None, root_directory)
    
    def tearDown(self):
        # Deactivate the testbed when completed
        self.testbed.deactivate()

#
# Handler Test Class
#

class HandlerTestCase(DatastoreTestCase):
    def setUp(self):
        # Call super to set up the testbed
        super(HandlerTestCase, self).setUp()
        
        # Wrap the app in the webtest.TestApp so handlers can be tested
        self.testapp = webtest.TestApp(app)


#
# Deferred Task Test Class
#

class DeferredTaskTestCase(HandlerTestCase):
    def setUp(self):
        # Call super to set up the testbed
        super(DeferredTaskTestCase, self).setUp()

        # Init the taskqueue stub
        self.testbed.init_taskqueue_stub()
        
        # Get the taskqueue stub
        self.taskqueue_stub = apiproxy_stub_map.apiproxy.GetStub('taskqueue')
    

    def execute_deferred(self):
        tasks = self.taskqueue_stub.GetTasks('default')
        self.taskqueue_stub.FlushQueue('default')
        while tasks:
            for task in tasks:
                (func, args, opts) = pickle.loads(base64.b64decode(task['body']))
                func(*args)
            
            tasks = self.taskqueue_stub.GetTasks('default')
            self.taskqueue_stub.FlushQueue('default')
