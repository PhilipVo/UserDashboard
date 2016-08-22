from system.core.router import routes

# Users
routes['default_controller'] = 'Users'
routes['GET']['/signin'] = 'Users#signin'
routes['GET']['/register'] = 'Users#register'
routes['GET']['/logout'] = 'Users#logout'
routes['GET']['/users/new'] = 'Users#new'
routes['GET']['/users/edit'] = 'Users#edit'
routes['GET']['/users/edit/<int:user_id>'] = 'Users#edit'
routes['GET']['/users/remove/<int:user_id>'] = 'Users#remove'
routes['GET']['/users/show/<int:user_id>'] = 'Users#show'
routes['GET']['/dashboard/'] = 'User#dashboard'
routes['GET']['/dashboard/admin'] = 'User#dashboard_admin'

routes['POST']['/Users/signin_user'] = 'Users#signin_user'
routes['POST']['/Users/register_user'] = 'Users#register_user'
routes['POST']['/Users/new_user'] = 'Users#new_user'
routes['POST']['/users/edit_info/<int:user_id>'] = 'Users#edit_info'
routes['POST']['/users/edit_password/<int:user_id>'] = 'Users#edit_password'
routes['POST']['/users/edit_description/<int:user_id>'] = 'Users#edit_description'

# Messages
routes['GET']['/messages/delete/<int:user_id>/<int:message_id>'] = 'Messages#delete'
routes['POST']['/messages/post/<int:receiver_id>'] = 'Messages#post'

# Comments
routes['GET']['/comments/delete/<int:user_id>/<int:comment_id>'] = 'Comments#delete'
routes['POST']['/comments/post/<int:user_id>/<int:message_id>'] = 'Comments#post'