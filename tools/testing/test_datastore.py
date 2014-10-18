import random
import unittest
from classes import DatastoreTestCase
from www.base.handlers import MemcacheHandler
from db.Email import Email

class DatastoreTests(DatastoreTestCase, MemcacheHandler):

	def test_add(self):
		#Simply adds one email to datastore
		a = Email.add({"email":"this@is.myemail"})
		self.assertNotEqual(a, False)

	def test_add_multiple(self):
		#b should not be added because it conflicts with a
		a = Email.add({"email":"this@is.myemail"})
		b = Email.add({"email":"this@is.myemail"})
		self.assertEqual(b, False)
