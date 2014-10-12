#!/usr/bin/python
import optparse, sys, os, unittest
from Datastore_tests import TestSequenceFunctions



def main(sdk_path, test_path, test='*'):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    suite = unittest.loader.TestLoader().discover(test_path, "test_" + test)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser("")
    options, args = parser.parse_args()
    
    #you may need to change these paths
    SDK_PATH = '/usr/local/google_appengine'
    TEST_PATH = '/YOUR-PATH-TO/hackillinois-website-2015/www/tests'

    if len(args) == 1:
        if args[0] == 'all':
            main(SDK_PATH, TEST_PATH)
        else:
            main(SDK_PATH, TEST_PATH, args[0])
    else:
        main(SDK_PATH, TEST_PATH)