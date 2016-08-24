from __future__ import print_function
from system.core.model import Model
import sys

class Comment(Model):
	def __init__(self):
		super(Comment, self).__init__()

	def delete_comment(self, id):
		query = "DELETE FROM comments where id = :id"
		data = {'id': id}
		self.db.query_db(query, data)
		return {'log': ['Sucessfully deleted comment.']}

	def delete_message_comments(self, message_id):
		query = "DELETE FROM comments where message_id = :message_id"
		data = {'message_id': message_id}
		return self.db.query_db(query, data)

	def delete_user_comments(self, user_id):
		query = "DELETE FROM comments where user_id = :user_id"
		data = {'user_id': user_id}
		return self.db.query_db(query, data)		

	def post_comment(self, dat, user_id, receiver_id, message_id):
		log = []

		if len(dat['comment']) == 0:
			log.append('Error: a comment cannot be blank.')
			return {'status': False, 'log': log}			

		query = """INSERT INTO comments (user_id, receiver_id, message_id, comment, created_at, updated_at)
					VALUES (:user_id, :receiver_id, :message_id, :comment, NOW(), NOW())
				"""
		data = {	'user_id': user_id,
					'receiver_id': receiver_id,
					'message_id': message_id,
					'comment': dat['comment']
				}
		self.db.query_db(query, data)
		log.append('Sucessfully posted new comment.')
		return {'status': True, 'log': log}

	def get_comments(self, receiver_id):
		query = """SELECT *, comments.id as id, CONCAT(first_name, ' ', last_name) AS name,
					comments.user_id as user_id,
					DATE_FORMAT(comments.created_at, '%M %D, %Y (%H:%i %p)') as comment_date 
					FROM comments LEFT JOIN messages ON comments.message_id = messages.id
					LEFT JOIN users on comments.user_id = users.id
					WHERE comments.receiver_id = :receiver_id
					ORDER BY comments.created_at ASC
				"""
		data = {'receiver_id': receiver_id}
		return self.db.query_db(query, data)	
