from __future__ import print_function
from system.core.model import Model
import re, sys

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def login_user(self, data):
		log = []

		for key, value in data.iteritems():
			if len(value) == 0:
				log.append('Login fail: email/password cannot be empty.')
				return {'status': False, 'log': log}

		query = """SELECT * FROM users
					WHERE email = :email LIMIT 1
				"""		
		user = self.db.query_db(query, data)

		# If registered email found:
		if len(user) != 0:
			# Check if password is correct:
			if self.bcrypt.check_password_hash(user[0]['password'], data['password']):
				log.append('Login successful!')				
				return {'status': True, 'log': log, 'user': user[0]}
			# Incorrect password:
			else:
				log.append('Login failed: incorrect password, please try again.')
				return {'status': False, 'log': log}

		# Else email not registered:
		else:
			log.append('Login failed: email not found, please register.')
			return {'status': False, 'log': log}

	def register_user(self, data):
		log = []

		# Check if any fields are empty:				
		for key, value in data.iteritems():
			if len(value) == 0:
				log.append('Registration failed: please fill in all form fields.')
				return {'status': False, 'log': log}

		# Check for valid first name:
		if len(data['first_name']) < 2 or not data['first_name'].isalpha():
			log.append('Registration failed: please enter a valid first name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid last name:
		if len(data['last_name']) < 2 or not data['last_name'].isalpha():
			log.append('Registration failed: please enter a valid last name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid email:
		if not EMAIL_REGEX.match(data['email']):
			log.append("Registration failed: please enter a valid email (example: name@mailserver.com)")
			return {'status': False, 'log': log}

		# Check if the email is a new/unique entry:
		query = """SELECT email FROM users
					WHERE email = :email LIMIT 1
				"""
		if len(self.db.query_db(query, data)) > 0:
			log.append("Registration failed: email already registered, please log in.")
			return {'status': False, 'log': log}

		# Check password length:
		if len(data['password']) < 8:
			log.append('Registration failed: password must be at least 8 characters long.')
			return {'status': False, 'log': log}

		# Check if the password matches the confirmation:
		if data['password'] != data['confirm_password']:
			log.append('Registration failed: password confirmation does not match.')
			return {'status': False, 'log': log}

		# All conditions met. Encrypt password and add to database:
		data['password'] = self.bcrypt.generate_password_hash(data['password'])
		query = """	INSERT INTO users (first_name, last_name, email,
					password, created_at, updated_at)
					VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())
				"""
		user = {'id': self.db.query_db(query, data)}
		log.append('Login successful!')				
		return {'status': True, 'log': log, 'user': user}

	def get_user(self, id):
		data = {'id': id}
		query = "SELECT * from users WHERE id = :id"
		return self.db.query_db(query, data)[0]
