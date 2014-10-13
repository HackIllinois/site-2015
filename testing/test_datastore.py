import random
import unittest
from classes import DatastoreTestCase
from db.Email import Email

class test_tests(DatastoreTestCase):

    def test_shuffle(self):
    	a = Email.add({"email":"this@is.myemail"})
    	print a
        self.assertEqual(1,1)
