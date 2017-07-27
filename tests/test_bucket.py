from unittest import TestCase

from classes.buckets import Buckets

class TestBucket(TestCase):

	def setUp(self):
		self.bucket = Buckets("first bucket")

	def test_bucket_created(self):
		"""test if a bucket is created successfully"""
		self.assertTrue(self.bucket.title == "first bucket", 
			"The bucket title shoud be set")

	def test_bucket_id(self):
		#test if each bucket is assigned an id
		self.assertTrue(self.bucket.id != None, "set an id to each bucket")
	
	def test_update_bucket(self):
		self.assertEqual(self.bucket.update_bucket(""), 
			"The new title cannot be empty.")

		#check if the title is updated successfully
		self.bucket.update_bucket("updated title")
		self.assertTrue(self.bucket.title == "updated title",
			"method update_bucket should update the title")

	def test_bucket_activity_create_activity(self):
		acivity_id = self.bucket.create_activity("first one")
		self.assertTrue(self.bucket.bucket_activities == [{
			'id': acivity_id,
			'title': "first one",
			"done": False
		}], "an item should be created")
	
	def test_activity_title(self):
		self.assertTrue(self.bucket.create_activity(""), 
			"The title cannot be empty")

	def test_bucket_update_activity(self):
		activity_id = self.bucket.create_activity("new activity")
		self.bucket.update_activity(activity_id, "newer ones")
		self.assertTrue(self.bucket.bucket_activities == 
			[{
				'id': activity_id,
				'title': 'newer ones',
				'done': False
			}], "The bucket_activities should be updated to 'newer ones'.")

	def test_delete_activity(self):
		activity_id = self.bucket.create_activity("remove this")
		activities_in_bucket = len(self.bucket.bucket_activities)
		self.bucket.delete_activity(activity_id)

		#check if activity has been deleted
		self.assertTrue(len(self.bucket.bucket_activities) == activities_in_bucket - 1,)


if __name__ == '__main__':
	unittest.main()
