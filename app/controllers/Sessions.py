from system.core.controller import *

# Sessions
routes['default_controller'] = 'Sessions'
routes['GET']['/signin'] = 'Sessions#signin'
routes['GET']['/register'] = 'Sessions#register'
routes['GET']['/logout'] = 'Sessions#logout'
routes['POST']['/signin_user'] = 'Sessions#signin_user'
routes['POST']['/register_user'] = 'Sessions#register_user'

# Dashboards
routes['GET']['/dashboard/'] = 'Dashboards'
routes['GET']['/dashboard/admin'] = 'Dashboards#admin'

# Users
routes['GET']['/users/new'] = 'Users#new'
routes['GET']['/users/edit'] = 'Users#edit'
routes['GET']['/users/edit/<int:user_id>'] = 'Users#edit'
routes['GET']['/users/show/<int:user_id>'] = 'Users#show'
routes['POST']['/users/new_user'] = 'Users#new_user'
routes['POST']['/users/edit_info/<int:user_id>'] = 'Users#edit_info'
routes['POST']['/users/edit_password/<int:user_id>'] = 'Users#edit_password'
routes['POST']['/users/edit_description/<int:user_id>'] = 'Users#edit_description'
routes['POST']['/users/remove_user/<int:user_id>'] = 'Users#remove_user'

# Messages
routes['GET']['/messages/delete_message/<int:message_id>'] = 'Messages#delete_message'
routes['POST']['/messages/post_message/<int:user_id>'] = 'Messages#post_message'

# Comments
routes['GET']['/comments/delete_comment/<int:comment_id>'] = 'Comments#delete_comment'
routes['POST']['/comments/post_comment/<int:user_id>'] = 'Comments#post_comment'


class Sessions(Controller):
	def __init__(self, action):
		super(Sessions, self).__init__(action)
		self.load_model('Session')
		self.load_model('User')
		self.db = self._app.db

	def index(self):
		return self.load_view('sessions/index.html')

	def signin(self):
		return self.load_view('sessions/singin.html')

	def register(self):
		return self.load_view('sessions/register.html')

	def logout(self):
		session.clear()
		return self.load_view('sessions/index.html')

	def signin_user(self):
		output = self.models['User'].signin_user(request.form)
		if output['status'] == True:
			session['user_id'] = output['user']['id']
			session['user_level'] = output['user']['level']
			for message in output['log']:
				flash(message, 'success')
			if session['user_level'] == 'Admin'
				return redirect('/dashboard/admin')			
			else:
				return redirect('/dashboard')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/signin')

	def register_user(self):
		output = self.models['Session'].register_user(request.form)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
			return redirect('/signin')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/register')