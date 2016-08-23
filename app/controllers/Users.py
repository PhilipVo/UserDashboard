from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')
		self.load_model('Message')
		self.load_model('Comment')
		self.db = self._app.db

	########## GET ##########
	def index(self):
		if session.get('user_level') == 'Normal':
			return redirect('/dashboard')			
		elif session.get('user_level') == 'Admin':
			return redirect('/dashboard/admin')
		return self.load_view('users/index.html')

	def signin(self):
		if session.get('user_id'):
			return redirect('/')
		return self.load_view('users/signin.html')

	def register(self):
		if session.get('user_id'):
			return redirect('/')				
		return self.load_view('users/register.html')

	def logout(self):
		session.clear()
		return redirect('/')

	def new(self):
		if session.get('user_level') == 'Admin':
			return render_template('users/new.html')
		else:		
			return redirect('/')

	def edit_self(self):
		if session.get('user_id'):
			return render_template('users/edit_self.html', user=self.models['User'].get_user(session['user_id']))
		else:
			return redirect('/')

	def edit_user(self, user_id):
		if session.get('user_level') == 'Admin':
			return render_template('users/edit_user.html', user=self.models['User'].get_user(user_id))
		else:
			return redirect('/')

	def remove(self, user_id):
		if session.get('user_level') == 'Admin':
			self.models['Comment'].delete_user_comments(user_id)
			self.models['Messages'].delete_user_messages(user_id)
			output = self.models['User'].remove_user(user_id)			
			for message in output['log']:
				flash(message, 'success')
			return redirect('/dashboard/admin')
		else:
			return redirect('/')

	def show(self, user_id):
		if session.get('user_id'):
			user = self.models['User'].get_user(user_id)
			messages = self.models['Message'].get_messages(user_id)
			comments = self.models['Comment'].get_comments(user_id)
			return render_template('users/show.html', user=user, messages=messages, comments=comments)
		else:
			return redirect('/')

	def dashboard(self):
		if session.get('user_level') == 'Normal':
			return render_template('users/dashboard.html', users=self.models['User'].get_users())
		elif session.get('user_level') == 'Admin':
			return redirect('/dashboard/admin')
		else:
			return redirect('/')

	def dashboard_admin(self):
		if session.get('user_level') == 'Admin':
			return render_template('users/dashboard_admin.html', users=self.models['User'].get_users())
		elif session.get('user_level') == 'Normal':
			return redirect('/dashboard')
		else:
			return redirect('/')

	########## POST ##########
	def signin_user(self):
		output = self.models['User'].signin_user(request.form)
		if output['status'] == True:
			session['user_id'] = output['user']['id']
			session['user_level'] = output['user']['level']
			return redirect('/')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/signin')

	def register_user(self):
		output = self.models['User'].register_user(request.form)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
			return redirect('/signin')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/register')

	def new_user(self):
		output = self.models['User'].new_user(request.form)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
			return redirect('/dashboard/admin')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/users/new')	

	def edit_info(self, user_id):
		output = self.models['User'].edit_info(request.form, user_id)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
		else:
			for message in status['log']:
				flash(message, 'error')

		if user_id == session['user_id']:
			return redirect('/users/edit')
		else:
			return redirect('/users/edit/{}'.format(user_id))

	def edit_password(self, user_id):
		output = self.models['User'].edit_password(request.form, user_id)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
		else:
			for message in status['log']:
				flash(message, 'error')
		
		if user_id == session['user_id']:
			return redirect('/users/edit')
		else:
			return redirect('/users/edit/{}'.format(user_id))

	def edit_description(self, user_id):
		output = self.models['User'].edit_description(request.form, user_id)
		for message in output['log']:
			flash(message, 'success')		
		return redirect('/users/edit')