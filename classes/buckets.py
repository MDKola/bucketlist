import time


class Buckets(object):

    def __init__(self, title):
        self.title = title
        self.bucket_activities = []

        epoch_time = time.time()
        self.id = round(float(str(epoch_time)[8:]) * 10000000)

    def create_activity(self, title):
        """Create an activity for the selected bucketlist"""
        epoch_time = time.time()
        activity_id = round(float(str(epoch_time)[8:]) * 10000000)

        activity = {
            "id": activity_id,
            "title": title,
            "done": False
        }
        self.bucket_activities.append(activity)
        return activity_id

    def update_bucket(self, new_title):
        """Update the bucketlist"""
        if len(new_title) < 1:
            return "The new title cannot be empty."
        # set new_title to title
        self.title = new_title

    def update_activity(self, id, new_activity_name):
        """Update the bucketlist activities"""
        count = 0

        for activity in self.bucket_activities:
            if str(id) == str(activity['id']):
                activity['title'] = new_activity_name
                self.bucket_activities.pop(count)
                self.bucket_activities.append(activity)
            count = + 1

    def delete_activity(self, id):
        """Delete a bucketlist activity"""
        activity_exist = False
        count = 0

        for activity in self.bucket_activities:
            if str(id) == str(activity["id"]):
                activity_exist = True
                self.bucket_activities.pop(count)

        count += 1

        if not activity_exist:
            return "activity does not exist"
