import random
import unittest
from classes import DatastoreTestCase
from db.Email import Email

class tests(DatastoreTestCase):

	def test_pass(self):
		self.assertEqual(1,1)

	def test_fail(self):
		self.assertEqual(1,2)

	def test_two(self):
		a = Email.add({"email":"this@is.myemail"})
		#a should be in the local datastore, but it doesn't show up
		self.assertNotEqual(a, False)

	def test_three(self):
		a = Email.add({"email":"this@is.myemail"})
		b = Email.add({"email":"this@is.myemail"})
		#a should be in the local datastore, but it doesn't show up
		self.assertEqual(b, False)
