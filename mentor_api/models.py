from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token
# Create your models here.


class User(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    phone = models.CharField(max_length=20,null=True, blank=True)
    Bio = models.TextField(null=True, blank=True)
    birthD = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=20,null=True, blank=True)
    city = models.CharField(max_length=20,null=True, blank=True)
    track = models.CharField(max_length=50,null=True, blank=True)
    intersts = models.CharField(max_length=200,null=True, blank=True)


    def __str__(self):
        return self.username
    


@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created= False,**kwargs):
    if created:
        Token.objects.create(user = instance)

class Mentor(models.Model):
    user = models.OneToOneField(User, related_name='Mentor', on_delete=models.CASCADE)
    track = models.CharField(max_length=100,default='web')

    def __str__(self):
        return self.user.username   
    
class Student(models.Model):
    user = models.OneToOneField(User, related_name='Student',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username   
    

class Request(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

class Session(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_sessions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_sessions')
    request = models.OneToOneField(Request, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField()
    zoom_link = models.CharField(max_length=255)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Session {self.id}'