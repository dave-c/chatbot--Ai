from django.db import models
from django.contrib.auth.models import User

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name

# User Profile Model with Role Choices and Courses
class UserProfile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        ADMIN = 'admin', 'Admin'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=Role.choices)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.username
    
# Student Progress Model with Points, Badges, and Level
class StudentProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badges = models.TextField(default="")
    level = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} Progress'

# Quiz Model with Multiple Options as a Foreign Key
class Quiz(models.Model):
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question

# Option Model for Multiple Quiz Options (Improved Structure)
class Option(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
