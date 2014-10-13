#!/usr/bin/python
import optparse, sys, os, unittest

def main(sdk_path, test_path, test='*'):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    print "ZZZZZZ"
    print dev_appserver
    suite = unittest.loader.TestLoader().discover(test_path, "test_" + test)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser("")
    options, args = parser.parse_args()
    
    SDK_PATH = '/usr/local/google_appengine'#For Mac OS X
    TEST_PATH = os.path.dirname(__file__)
    print "TEST_PATH: " + TEST_PATH
    
    if len(args) == 1:
        if args[0] == 'all':
            main(SDK_PATH, TEST_PATH)
        else:
            main(SDK_PATH, TEST_PATH, args[0])
    else:
        main(SDK_PATH, TEST_PATH)