from system.core.controller import *

class Products(Controller):
	def __init__(self, action):
		super(Products, self).__init__(action)
		self.load_model('Product')
		self.db = self._app.db

	def index(self):
		return self.load_view('index.html', products=self.models['Product'].get_products())

	def new(self):
		return self.load_view('new.html')

	def edit(self, id):
		return self.load_view('edit.html', product=self.models['Product'].get_product(id))

	def show(self, id):
		return self.load_view('show.html', product=self.models['Product'].get_product(id))

	def create(self):
		status = self.models['Product'].create_product(request.form)
		if status['status'] == True:
			for message in status['log']:
				flash(message, 'success')			
			return redirect('/')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/products/new')

	def update(self, id):
		status = self.models['Product'].update_product(id, request.form)
		if status['status'] == True:
			for message in status['log']:
				flash(message, 'success')			
			return redirect('/')
		else:
			for message in status['log']:
				flash(message, 'error')
			return redirect('/products/edit/{}'.format(id))

	def destroy(self, id):
		self.models['Product'].destroy_product(id)
		return redirect('/products')