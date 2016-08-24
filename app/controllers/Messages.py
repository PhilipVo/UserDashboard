from system.core.controller import *

class Messages(Controller):
	def __init__(self, action):
		super(Messages, self).__init__(action)
		self.load_model('Message')
		self.load_model('Comment')
		self.db = self._app.db

	########## GET ##########
	def delete(self, user_id, message_id):
		self.models['Comment'].delete_message_comments(message_id)
		output = self.models['Message'].delete_message(message_id)
		for message in output['log']:
			flash(message, 'success')
		return redirect('/users/show/{}'.format(user_id))		


	########## POST ##########
	def post(self, receiver_id):
		output = self.models['Message'].post_message(request.form, session['user_id'], receiver_id)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
		else:
			for message in status['log']:
				flash(message, 'error')
		return redirect('/users/show/{}'.format(receiver_id))		
