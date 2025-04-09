from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.username
    
class StudentProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badges = models.TextField(default="")
    level = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} Progress'



# Create your models here.
