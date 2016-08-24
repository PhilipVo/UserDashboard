from __future__ import print_function
from system.core.model import Model
import re, sys

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def get_user(self, id):
		data = {'id': id}
		query = "SELECT *, DATE_FORMAT(created_at, '%b %d, %Y') AS user_date FROM users WHERE id = :id"
		return self.db.query_db(query, data)[0]		

	def get_users(self):
		query = "SELECT *, DATE_FORMAT(created_at, '%b %d, %Y') AS user_date FROM users"
		return self.db.query_db(query)		
	
	def remove_user(self, id):
		query = "DELETE FROM users WHERE id = :id"
		data = {'id': id}
		self.db.query_db(query, data)		
		return {'log': ['Successfully removed user.']}

	def signin_user(self, data):
		log = []

		for key, value in data.iteritems():
			if len(value) == 0:
				log.append('Login error: email/password cannot be empty.')
				return {'status': False, 'log': log}

		query = "SELECT * FROM users WHERE email = :email LIMIT 1"		
		user = self.db.query_db(query, data)

		# If registered email found:
		if len(user) != 0:
			# Check if password is correct:
			if self.bcrypt.check_password_hash(user[0]['password'], data['password']):
				# log.append('Login successful!')				
				return {'status': True, 'log': log, 'user': user[0]}
			# Incorrect password:
			else:
				log.append('Login error: incorrect password, please try again.')
				return {'status': False, 'log': log}

		# Else email not registered:
		else:
			log.append('Login error: email not found, please register.')
			return {'status': False, 'log': log}

	def register_user(self, data):
		log = []

		# Check if any fields are empty:				
		for key, value in data.iteritems():
			if len(value) == 0:
				log.append('Registration error: please fill in all form fields.')
				return {'status': False, 'log': log}

		# Check for valid first name:
		if len(data['first_name']) < 2 or not data['first_name'].isalpha():
			log.append('Registration error: please enter a valid first name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid last name:
		if len(data['last_name']) < 2 or not data['last_name'].isalpha():
			log.append('Registration error: please enter a valid last name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid email:
		if not EMAIL_REGEX.match(data['email']):
			log.append("Registration error: please enter a valid email (example: name@mailserver.com)")
			return {'status': False, 'log': log}

		# Check if the email is a new/unique entry:
		query = "SELECT email FROM users WHERE email = :email LIMIT 1"
		if len(self.db.query_db(query, data)) > 0:
			log.append("Registration error: email already registered, please log in.")
			return {'status': False, 'log': log}

		# Check password length:
		if len(data['password']) < 8:
			log.append('Registration error: password must be at least 8 characters long.')
			return {'status': False, 'log': log}

		# Check if the password matches the confirmation:
		if data['password'] != data['password_confirmation']:
			log.append('Registration error: password confirmation does not match.')
			return {'status': False, 'log': log}

		# Set user level:
		query = "SELECT * FROM users LIMIT 1"
		if len(self.db.query_db(query)) == 0:
			level = 'Admin'		
		else:
			level = 'Normal'

		dat = {'level': level}
		for key, value in data.iteritems():
			dat[key] = value

		# All conditions met. Encrypt password:
		dat['password'] = self.bcrypt.generate_password_hash(dat['password'])
		print(dat, file=sys.stderr)
		# Add to database:
		query = """INSERT INTO users (first_name, last_name, email,
							password, level, created_at, updated_at)
							VALUES (:first_name, :last_name, :email, :password, :level, NOW(), NOW())
						"""
		user = {'id': self.db.query_db(query, dat)}
		log.append('Thank you for registering! Please login to continue.')				
		return {'status': True, 'log': log, 'user': user}

	def new_user(self, data):
		log = []

		# Check if any fields are empty:				
		for key, value in data.iteritems():
			if len(value) == 0:
				log.append('Error: please fill in all form fields.')
				return {'status': False, 'log': log}

		# Check for valid first name:
		if len(data['first_name']) < 2 or not data['first_name'].isalpha():
			log.append('Error: please enter a valid first name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid last name:
		if len(data['last_name']) < 2 or not data['last_name'].isalpha():
			log.append('Error: please enter a valid last name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid email:
		if not EMAIL_REGEX.match(data['email']):
			log.append("Error: please enter a valid email (example: name@mailserver.com)")
			return {'status': False, 'log': log}

		# Check if the email is a new/unique entry:
		query = "SELECT email FROM users WHERE email = :email LIMIT 1"
		if len(self.db.query_db(query, data)) > 0:
			log.append("Error: email already registered, please log in.")
			return {'status': False, 'log': log}

		# Check password length:
		if len(data['password']) < 8:
			log.append('Error: password must be at least 8 characters long.')
			return {'status': False, 'log': log}

		# Check if the password matches the confirmation:
		if data['password'] != data['password_confirmation']:
			log.append('Error: password confirmation does not match.')
			return {'status': False, 'log': log}

		# Set user level:
		dat = {'level': 'Normal'}

		for key, value in data.iteritems():
			dat[key] = value

		# All conditions met. Encrypt password:
		dat['password'] = self.bcrypt.generate_password_hash(dat['password'])

		# Add to database:
		query = """INSERT INTO users (first_name, last_name, email,
							password, level, created_at, updated_at)
							VALUES (:first_name, :last_name, :email, :password, :level, NOW(), NOW())
						"""
		user = {'id': self.db.query_db(query, dat)}
		log.append('{} {} has been added!'.format(data['first_name'], data['last_name']))
		return {'status': True, 'log': log, 'user': user}

	def edit_info(self, dat, id):
		log = []
		data = {'id': id}

		for key, value in dat.iteritems():
			data[key] = value

		# Check for valid first name:
		if len(data['first_name']) < 2 or not data['first_name'].isalpha():
			log.append('Error: please enter a valid first name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid last name:
		if len(data['last_name']) < 2 or not data['last_name'].isalpha():
			log.append('Error: please enter a valid last name (letters only).')
			return {'status': False, 'log': log}

		# Check for valid email:
		if not EMAIL_REGEX.match(data['email']):
			log.append("Error: please enter a valid email (example: name@mailserver.com)")
			return {'status': False, 'log': log}

		new = "SELECT email FROM users WHERE email = :email LIMIT 1"
		old = "SELECT email FROM users WHERE id = :id LIMIT 1"

		new_email = self.db.query_db(new, data)
		old_email = self.db.query_db(old, data)

		# Update user with valid information:
		if len(new_email) == 0 or new_email == old_email:
			query = """UPDATE users SET first_name = :first_name, last_name = :last_name,
						email = :email, level = :level, updated_at = NOW() WHERE id = :id
					"""
			self.db.query_db(query, data)
			log.append('Information updated for {} {}.'.format(data['first_name'], data['last_name']))
			return {'status': True, 'log': log}						
		else:
			log.append('Error: email already in use.')
			return {'status': False, 'log': log}

	def edit_password(self, dat, id):
		log = []
		data = {'id': id}

		for key, value in dat.iteritems():
			data[key] = value

		# Check password length:
		if len(data['password']) < 8:
			log.append('Error: password must be at least 8 characters long.')
			return {'status': False, 'log': log}

		# Check if the password matches the confirmation:
		if data['password'] != data['password_confirmation']:
			log.append('Error: password confirmation does not match.')
			return {'status': False, 'log': log}

		# All conditions met. Encrypt password and update:
		query = "UPDATE users SET password = :password, updated_at = NOW() WHERE id = :id"
		self.db.query_db(query, data)
		log.append('Password updated.')
		return {'status': True, 'log': log}	

	def edit_description(self, dat, id):
		log = []
		data = {'id': id}

		for key, value in dat.iteritems():
			data[key] = value

		query = "UPDATE users SET description = :description, updated_at = NOW() WHERE id = :id"
		self.db.query_db(query, data)
		log.append('Description updated.')
		return {'status': True, 'log': log}	