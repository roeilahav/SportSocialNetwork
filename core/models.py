from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth.models import User

import json 

# User = get_user_model()
SPORTS_ITEM = (
    ('SOCCER','SOCCER'),
    ('BASKETBALL','BASKETBALL'),
    ('TENNIS','TENNIS'),
    ('CYCLING','CYCLING'),
)
LAVEL = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)
GENDER = (
    ('MALE','MALE'),	
    ('FEMALE','FEMALE') 
)

LOCATION = (
    ('TEL AVIV','TEL AVIV'),
    ('BEER SHEVA','BEER SHEVA'),
    ('JERUSALEM','JERUSALEM'),
    ('HAIFA','HAIFA'),
    ('DIMONA','DIMONA'),
    ('RAMAT GAN','RAMAT GAN'),
    ('HERZELIA','HERZELIA'),
    ('HEDERA','HEDERA'),
    ('KIRIAT SHMONA','KIRIAT SHMONA'),
    ('ELIAT','ELIAT')
)
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100,choices = LOCATION, blank=True)
    age = models.IntegerField(blank=True,null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER, default='MALE', blank=True, null=True)
    sport = models.CharField(
        max_length=20, choices=SPORTS_ITEM, default='SOCCER', blank=True, null=True)
    level = models.CharField(
        max_length=2, choices=LAVEL, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    number_of_new = models.IntegerField(default=0)
    #list for preferences of user 
    #[ ["Morning" , 2] , []]
    preferences = models.CharField(max_length=10000, blank=True, null=True)
    rating = models.IntegerField(default=5)
    
    def setPreferences(self,preferences):
        self.preferences = json.dumps(preferences)

    def getPreferences(self):
        return self.preferences
    


    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
RATING=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)

class Feedback(models.Model):
    q1 = models.CharField(max_length=200,blank=True)
    a1 = models.IntegerField(max_length=5,blank=True,choices=RATING )
    q2 = models.CharField(max_length=200,blank=True)
    a2 = models.IntegerField(max_length=5,blank=True,choices=RATING )
    q3 = models.CharField(max_length=200,blank=True)
    a3 = models.IntegerField(max_length=5,blank=True,choices=RATING )
    q4 = models.CharField(max_length=200,blank=True)
    a4 = models.IntegerField(max_length=5,blank=True,choices=RATING )
    q5 = models.CharField(max_length=200,blank=True)
    a5 = models.IntegerField(max_length=5,blank=True,choices=RATING )
    msg = models.TextField(blank=True , null=True) 
    
    def __str__(self):
        return f'feedback-{self.id}'
    
    def get_average_rating(self):
        return (self.a1+self.a2+self.a3+self.a4+self.a5) / 5

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    event_name = models.CharField(max_length=100,blank=True)
    sport = models.CharField(max_length=20, choices=SPORTS_ITEM)
    lavel = models.CharField(max_length=20,default=0,blank=True) 
    location = models.CharField(max_length=100, choices=LOCATION ,blank=True) 
    no_of_participents = models.IntegerField(default=0)
    participant_left = models.IntegerField(default=0,blank=True) 
    date = models.DateField(auto_now=False, auto_now_add=False) 
    time = models.TimeField(auto_now=False, auto_now_add=False)  
    image = models.ImageField(upload_to='event_image/',blank=True)
    participants = models.ManyToManyField(Profile,blank=True)
    feedbacks = models.ManyToManyField(Feedback, blank=True)

    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.sport 
    
    def join_event(self, user):
        self.participants.add(user)


# class contact_feeback(models.Model):
#     who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who')
#     to_whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_whom')
#     a1 = models.TextField(blank=True)

    
class Feedback2(models.Model):
    a1 = models.TextField(blank=True) 
    

class Notification(models.Model):
    notification_of = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.IntegerField(default=0)
    noti_text = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)
    who_contacted = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='who_contacted')
    
