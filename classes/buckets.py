import time


class Item(object):

	def __init__(self, item_name):
		#generate random identifier for the item
		epoch_time = time.time()
		self.identifier = round(float(str(epoch_time)[8:]) * 10000000)
		self.title = item_name
		self.completed = False

class Buckets(object):

	def __init__(self):
		self.title = title
		self.progress = None
		self.priority = 1
		self.my_buckets = []

		#generate id for bucketlist
		epoch_time = time.time()
		self.id = round(float(str(epoch_time)[8:])*10000000)

	def set_priority(self, priority):
		#validate priority input to integers only
		if not isinstance(priority, int):
			return "Please enter a number."
		self.priority = priority

	def set_progress(self, progress):
		self.progress = progress

	def update(self, updated_title):
		if len(updated_title) < 1:
			return 'The title must be more than one character.'
		self.title = title

	def create_item(self, item_name):
		if len(item_name) < 1:
			return 'Please Enter a valid name.'

		item = Item(item_name)
		self.items.append(item)
		return item.id

	def update_item(self, id, new_item_name):
		item_exists = False
		count = 0
		for item in self.items:
			if str(id) == str(item.id):
				#update item
				item_exists = True
				item.title = new_item_name

				#update list of items
				self.items.pop(count)
				self.items.append(item)
			count +=1
		if not item_exists:
			return 'Item does not exist.'

	def delete_item(self, id):
		item_exists = False
		count = 0
		for item in self.items:
			if str(id) == str(item.id):
				item_exists = True
				self.items.pop(count)

			count += 1
		if not item_exists:
			return 'Item Does Not Exist.'
		