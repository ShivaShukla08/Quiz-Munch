from django.contrib.auth.models import User
from django.db import models

#.........................................Not use................................................#
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
        
# ...................................Below present code in our use.................................#


class StudentsProfile(models.Model):
    user_id = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=45)
    roll_no = models.CharField(max_length=15)
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

class CoreStreams(models.Model):
    course_id = models.CharField(max_length=100)
    course_name = models.CharField(max_length=50)
    semester = models.IntegerField()
    stream = models.CharField(max_length=50)


class response_table(models.Model):
    uuid = models.UUIDField(unique=False)
    sap_id = models.CharField(max_length=25, unique=False)
    total_correct = models.IntegerField()
    total_incorrect = models.IntegerField()

    def __str__(self):  
        return self.sap_id
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.CharField(max_length=50)
    feedback = models.TextField()
    screenshot = models.ImageField(upload_to='feedback_screenshots/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# .≥≥≥≥≥≥≥≥≥≥≥≥≥≥Below code is of no use≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥.
class CoreStream(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=50)
    semester = models.IntegerField()
    stream = models.CharField(max_length=50)
#≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥≥.
