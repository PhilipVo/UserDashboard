from system.core.router import routes

# Sessions
routes['default_controller'] = 'Sessions'
routes['GET']['/signin'] = 'Sessions#signin'
routes['GET']['/register'] = 'Sessions#register'
routes['GET']['/logout'] = 'Sessions#logout'
routes['POST']['/signin_user'] = 'Sessions#signin_user'
routes['POST']['/register_user'] = 'Sessions#register_user'

# Dashboards
routes['GET']['/dashboards/'] = 'Dashboards'
routes['GET']['/dashboards/admin'] = 'Dashboards#admin'

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
