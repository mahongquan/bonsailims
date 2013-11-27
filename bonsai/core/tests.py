import unittest
from django.contrib import auth

class LdapAuthenticationTestCase (unittest.TestCase):
	
	username = 'sbozdag'
	password = 'GokseL687!_?'
	
	def testAuthenticating(self):
		error, user = auth.authenticate(self.username, self.password)
		self.assertEquals(error, None)
		 
		

