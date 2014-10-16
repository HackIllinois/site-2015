import random
import unittest
from classes import HandlerTestCase
from www.base.handlers import MemcacheHandler
from db.Email import Email

class IndexHandlerTests(HandlerTestCase, MemcacheHandler):

	def test_get(self):
		#Simply adds one email to datastore
		response = self.testapp.get('/')
		self.assertEqual(response.status_int, 200)

	def test_post(self):
		#b should not be added because it conflicts with a
		params = {"email":"this@is.myemail"}

		response = self.testapp.post('/', params)
		a = Email.search_database({"email":"this@is.myemail"})
		self.assertEqual(response.status_int, 200)
		self.assertEqual(len(a.fetch()), 1)
