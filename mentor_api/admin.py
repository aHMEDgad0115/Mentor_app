from django.contrib import admin
from .models import User, Mentor, Student,Session,Request,Review
# Register your models here.

admin.site.register(User)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Request)
admin.site.register(Review)