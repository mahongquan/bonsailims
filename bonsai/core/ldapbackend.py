from django.conf import settings
from django.contrib.auth.models import User, check_password
import ldap
import settings

class LdapBackend:
	SCOPE = ldap.SCOPE_SUBTREE
	RETRIEVE_ATTRIBUTES = None
	TIMEOUT = 0
	def authenticate(self, username=None, password=None):
	 	if username is None and password is None:
	 		return (ldap.INVALID_CREDENTIALS, None)
		connection = ldap.initialize('ldap://%s:%s' % (settings.LDAP_ADDRESS, settings.LDAP_PORT))		
		try:
			if settings.LDAP_TLS_ENABLED:
				connection.start_tls_s()	 	
			dn = 'cn=%s,%s' % (username, settings.LDAP_BIND_DN)			
			connection.simple_bind_s(dn, password)
			# authentication success
			try:
				user = User.objects.get(username=username)
			except User.DoesNotExist:	
				search_filter = "cn=" + username
				result_id = connection.search(settings.LDAP_BASE_DN, self.SCOPE, search_filter, self.RETRIEVE_ATTRIBUTES)		
				r_type, r_data = connection.result(result_id, self.TIMEOUT)
				forename = r_data[0][1][settings.LDAP_FIRSTNAME_ATTRIBUTE]
				lastname = r_data[0][1][settings.LDAP_LASTNAME_ATTRIBUTE]
				emailattr = r_data[0][1][settings.LDAP_EMAIL_ATTRIBUTE]
				sep = ' '
				user = User(username=username, password=password, 
			 				first_name=sep.join(forename), last_name=sep.join(lastname), email=emailattr[0])
			 	user.set_unusable_password()
			 	user.is_staff = True
			 	user.is_superuser = False
			 	user.save()

		except ldap.INVALID_CREDENTIALS:
			# TODO:instead of printing we need logging
			print '==>Invalid Credentials'
			return None
		except ldap.LDAPError, e:
			# TODO:instead of printing we need logging
			print '==>Error: %s' % e.message
			return None

		return user		 
		
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
	 
	def has_perm(self, user_obj, perm):
		# All permissions are granted
	 	# TODO: Revision needed
		return True
		
