from django.db import models
from django.contrib.auth.models import User       #class message

# Create your models here.

class Topic(models.Model):                            #topic can have multiple rooms but a room can have only multiple topics
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)    #since by default null is False
    participants=models.ManyToManyField(User, related_name='participants',blank=True)  #to be able to submit a form without having to check something
    updated=models.DateTimeField(auto_now=True)    #will take a time snap shot everytime we save the item
    created=models.DateTimeField(auto_now_add=True)    #will 

    class Meta:
        ordering=['-updated','-created']    # '-' indicates descending order. Query requests will be ordered by updated field first in descending order and then created order

    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)  #Room being the parent class. On deletion of the parent class, all the msgs are to be deleted. This is one project to many reviews type
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)   
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.body[0:50]