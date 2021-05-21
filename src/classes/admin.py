from django.contrib import admin

from .models import Classroom, Classwork, Submission,  Post

# Register your models here.
admin.site.register(Classroom)
admin.site.register(Classwork)
admin.site.register(Submission)
admin.site.register(Post)

