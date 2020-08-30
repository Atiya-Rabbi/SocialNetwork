from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Allpost(models.Model):
	"""keep track of all posts"""
	postadmin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	postdate = models.CharField(max_length=100)
	likes = models.IntegerField()
	post = models.TextField()

	def __str__(self):
		return f"{self.postadmin}: [{self.postdate}, {self.likes}, {self.post}]"

class Post_liked(models.Model):
	"""keep track of all posts liked by the user"""
	username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	postliked = models.ManyToManyField(Allpost,null=True,blank=True)
	
	def __str__(self):
		return f"{self.username}:[{self.postliked}]"
		
class Following(models.Model):
	"""keep track of the followings of user"""
	username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="followings")
	following = models.ManyToManyField(User, blank=True)

	def __str__(self):
		return f"{self.username}: [{self.following}]"

class Follower(models.Model):
	"""keep track of user's followers"""
	username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="followers")
	follower = models.ManyToManyField(User, blank=True)

	def __str__(self):
		return f"{self.username}: [{self.follower}]"
