from system.core.router import routes

# Users
routes['default_controller'] = 'Users'
routes['GET']['/signin'] = 'Users#signin'
routes['GET']['/register'] = 'Users#register'
routes['GET']['/logout'] = 'Users#logout'
routes['GET']['/users/new'] = 'Users#new'
routes['GET']['/users/edit'] = 'Users#edit_self'
routes['GET']['/users/edit/<int:user_id>'] = 'Users#edit_user'
routes['GET']['/users/remove/<int:user_id>'] = 'Users#remove'
routes['GET']['/users/show/<int:user_id>'] = 'Users#show'
routes['GET']['/dashboard/'] = 'Users#dashboard'
routes['GET']['/dashboard/admin'] = 'Users#dashboard_admin'

routes['POST']['/signin_user'] = 'Users#signin_user'
routes['POST']['/register_user'] = 'Users#register_user'
routes['POST']['/users/new_user'] = 'Users#new_user'
routes['POST']['/users/edit_info/<int:user_id>'] = 'Users#edit_info'
routes['POST']['/users/edit_password/<int:user_id>'] = 'Users#edit_password'
routes['POST']['/users/edit_description/<int:user_id>'] = 'Users#edit_description'

# Messages
routes['POST']['/messages/delete/<int:user_id>/<int:message_id>'] = 'Messages#delete'
routes['POST']['/messages/post/<int:receiver_id>'] = 'Messages#post'

# Comments
routes['POST']['/comments/delete/<int:user_id>/<int:comment_id>'] = 'Comments#delete'
routes['POST']['/comments/post/<int:receiver_id>/<int:message_id>'] = 'Comments#post'