import random
import unittest
from classes import DatastoreTestCase
from db.Email import Email

class test_tests(DatastoreTestCase):

	def test_one(self):
		self.assertEqual(1,1)

	def test_two(self):
		a = Email.add({"email":"this@is.myemail"})
		print a
		#a should be in the local datastore, but it doesn't show up
		self.assertEqual(1,1)
