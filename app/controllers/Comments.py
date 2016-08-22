from system.core.controller import *

routes['GET']['/comments/delete/<int:user_id>/<int:comment_id>'] = 'Comments#delete'
routes['POST']['/comments/post/<int:message_id>'] = 'Comments#post'

class Comments(Controller):
	def __init__(self, action):
		super(Comments, self).__init__(action)
		self.load_model('Comment')
		self.db = self._app.db

	########## GET ##########
	def delete(self, user_id, comment_id):
		output = self.models['Comment'].delete_comment(comment_id)
		for message in output['log']:
			flash(message, 'success')
		return redirect('/show/{}'.format(user_id))


	########## POST ##########
	def post(self, user_id, message_id):
		output = self.models['Comment'].post_comment(request.form, session['id'], user_id, message_id)
		if output['status'] == True:
			for message in output['log']:
				flash(message, 'success')
		else:
			for message in status['log']:
				flash(message, 'error')
		return redirect('/show/{}'.format(user_id))
