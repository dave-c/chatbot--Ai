from django.contrib import admin
from .models import Course, UserProfile, StudentProgress, Quiz, Option

admin.site.register(Course)
admin.site.register(UserProfile)
admin.site.register(StudentProgress)
admin.site.register(Quiz)
admin.site.register(Option)

