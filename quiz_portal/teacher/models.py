from django.db import models
import uuid

class TeacherProfile(models.Model):
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    personal_mail = models.EmailField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    def __str__(self):  
        return self.name

class TeacherCourse(models.Model):
    tid = models.CharField(max_length=36)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_id = models.CharField(max_length=20)
    batch = models.CharField(max_length=20)
    HONOR_CHOICES = [
        ('H', 'Honor'),
        ('NH', 'Non-Honor')
    ]
    honor_or_non_honor = models.CharField(max_length=2, choices=HONOR_CHOICES)

    def __str__(self):
        return f"{self.course_name} - {self.teacher.name}"



class Quiz_details(models.Model):
    teacher_id = models.CharField(max_length=100)
    quiz_name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    course_id = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)
    stream = models.CharField(max_length=100)
    backtracking = models.BooleanField(default=False)
    upload = models.BooleanField(default=False)
    
    def __str__(self):
        return self.quiz_name


class Quiz_Question_detail(models.Model):
    uuid = models.UUIDField(unique=False)
    question_number = models.PositiveIntegerField()
    question_description = models.TextField()
    question_type = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Question {self.question_number}: {self.question_description}"



#............................... Below code is of no use................................

class Quiz(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    quiz_number = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    batch = models.CharField(max_length=255)
    duration = models.IntegerField()
    def __str__(self):
        return f"Quiz {self.quiz_number}"



class QuizQuestion(models.Model):
    quiz_number = models.IntegerField(default=0)
    question_number = models.CharField(max_length=255)
    question_description = models.CharField(max_length=500)  # Add this line for the new column
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)

    def __str__(self):
        return f"Question {self.question_number}"



