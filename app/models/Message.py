from __future__ import print_function
from system.core.model import Model
import sys

class Message(Model):
	def __init__(self):
		super(Message, self).__init__()

	def delete_message(self, id):
		query = "DELETE FROM messages WHERE id = :id"
		data = {'id': id}
		self.db.query_db(query, data)
		return {'log': ['Sucessfully deleted message.']}

	def delete_user_messages(self, user_id):
		query = "DELETE FROM messages WHERE user_id = :user_id"
		data = {'user_id': user_id}
		return self.db.query_db(query, data)		

	def post_message(self, dat, user_id, receiver_id):
		log = []

		if len(dat['message']) == 0:
			log.append('Error: a message cannot be blank.')
			return {'status': False, 'log': log}			

		query = """INSERT INTO messages (user_id, receiver_id, message, created_at, updated_at)
					VALUES (:user_id, :receiver_id, :message, NOW(), NOW())
				"""
		data = {	'user_id': user_id,
					'receiver_id': receiver_id,
					'message': dat['message']
				}
		self.db.query_db(query, data)
		return {'status': True, 'log': ['Sucessfully posted new message.']}

	def get_messages(self, receiver_id):
		query = """SELECT *,  messages.id as id, CONCAT(first_name, ' ', last_name) AS name,
					DATE_FORMAT(messages.created_at, '%M %D, %Y (%H:%i %p)') as message_date 
					FROM messages LEFT JOIN users ON messages.user_id = users.id
					WHERE receiver_id = :receiver_id ORDER BY messages.created_at DESC
				"""
		data = {'receiver_id': receiver_id}
		return self.db.query_db(query, data)	
