from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    roll_no = models.CharField(max_length=15, unique=True)
    semester = models.IntegerField()
    stream = models.CharField(max_length=40)
    honor = models.CharField(max_length=10)
    major = models.CharField(max_length=30, null=True, blank=True)
    minor = models.CharField(max_length=30, null=True, blank=True)
    exploratory = models.CharField(max_length=30, null=True, blank=True)
    major_id = models.CharField(max_length=30)
    minor_id = models.CharField(max_length=30)
    exploratory_id = models.CharField(max_length=30)
    batch = models.CharField(max_length=10)
    course_duration = models.IntegerField()
    contact_no = models.BigIntegerField()
    personal_mail = models.EmailField()
    parents_contact_no = models.BigIntegerField()
    parents_email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class CoreStream(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=50)
    semester = models.IntegerField()
    stream = models.CharField(max_length=50)

