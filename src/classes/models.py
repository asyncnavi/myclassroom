from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
from uuid import uuid4
from django.utils import timezone
from django.contrib.humanize.templatetags import humanize


def get_uuid():
    s = str(uuid4())[:8]

    return s


User = get_user_model()

POST_CHOICES = (
    ('annoucement', 'announcement'),
    ('studymaterial', 'studymaterial')
)


class Classroom(models.Model):
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(default=get_uuid(), max_length=8, unique=True, editable=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='students', blank=True)
    created = models.DateField(auto_now=True)
    subject = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} by {self.teacher.name}"


class Post(models.Model):
    tittle = models.CharField(max_length=100, blank=False)
    type = models.CharField(choices=POST_CHOICES, max_length=30)
    detail = models.TextField(max_length=1000, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, )
    attached_file = models.FileField(upload_to="post", blank=True)
    created = models.DateTimeField(blank=True, default=timezone.now)

    def get_created(self):
        return humanize.naturaltime(self.created)

    def __str__(self):
        return f"{self.tittle} - {self.classroom.code}"


class Classwork(models.Model):
    tittle = models.CharField(max_length=100, blank=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    detail = models.TextField(max_length=1000, blank=True)
    attached_file = models.FileField(upload_to="classwork", blank=True)
    created = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.tittle} - {self.classroom.code}"


class Submission(models.Model):
    classwork = models.ForeignKey(Classwork, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    uploaded_file = models.FileField(upload_to="submission")
    is_submitted = models.BooleanField(default=False)
    created = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return f"{self.classwork.tittle} - {self.classwork.classroom.code} by {self.student.name}"
