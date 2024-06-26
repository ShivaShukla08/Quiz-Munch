# Generated by Django 4.2.6 on 2024-05-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_quizdetailsresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletionCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('certificated_id', models.UUIDField(unique=True)),
                ('sap_id', models.CharField(max_length=25)),
                ('correctMarks', models.CharField(max_length=100)),
                ('TotalMarks', models.CharField(max_length=100)),
                ('completion_date', models.DateField()),
            ],
        ),
    ]
