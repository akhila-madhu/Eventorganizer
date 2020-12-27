from django.db import models
from django.contrib.auth import models as django_models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_manager = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user) + '->' + str(self.is_manager)

class Event(models.Model):
    Name=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Eventname = models.CharField(max_length=200)
    thumbnail = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=200)
    body = body=models.TextField()
    venue = models.CharField(max_length=200)
    DateAndTime = models.DateTimeField()
    TotalAvailableSeats = models.IntegerField()
    
    def __str__(self):
        return self.Eventname 

    

