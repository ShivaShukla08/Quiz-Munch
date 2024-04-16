from django import forms
from .models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['quiz_number', 'name', 'course', 'batch', 'duration']

    quiz_number = forms.IntegerField(label='Quiz Number')
    name = forms.CharField(label='Quiz Name')
    course = forms.ChoiceField(choices=[('course1', 'Course 1'), ('course2', 'Course 2')], label='Course Name')
    batch = forms.CharField(label='Batch')
    duration = forms.IntegerField(label='Duration (in minutes)')
    quiz_file = forms.FileField(label='Quiz File', help_text='Upload a text file containing quiz questions.')
