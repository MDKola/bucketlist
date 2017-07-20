import time

class Buckets(object):

	def __init__(self, title):
		self.title = title
		self.progress = None
		self.bucket_activities = []
		
		epoch_time = time.time()
		self.id = round(float(str(epoch_time)[8:]) * 10000000)
	
	def progress(self, progress):
		self.progress = progress

	def create_activity(self, title):
		if len(title) < 0:
			return "The title cannot be empty"
		#generate a random id
		epoch_time = time.time()
		self.ativity_id = round(float(str(epoch_time)[8:]) * 10000000)

		activity = {
			"activity_id": id,
			"title": title,
			"done": False
		}
		self.bucket_activities.append(activity)
		return id


	def update_bucket(self, new_title):
		#validate if the new_title is valid
		if len(new_title) < 1:
			return "The new title cannot be empty."
		#set new_title to title
		self.title = new_title


	def update_activity(self, new_activity_name, id):
		activity_exist = False
		count = 0

		for activity in self.bucket_activities:
			if str(id) == str(activity['activity_id']):
				activity_exists = True
				activity['title'] = new_activity_name
				self.bucket_activities.pop(count)
				self.bucket_activities.append(activity)
			count =+ 1
		if not activity_exist:
			return "The item does not exist"

	def delete_activity(self, id):
		activity_exist = False
		count = 0

		for activity in self.bucket_activities:
			if str(id) == str(activity["activity_id"]):
				activity_exist = True
				self.bucket_activities.pop(count)

		count += 1

		if not activity_exist:
			return "activity does not exist"
	