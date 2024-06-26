# Generated by Django 4.1.7 on 2024-03-09 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoreStream',
            fields=[
                ('course_id', models.IntegerField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=50)),
                ('semester', models.IntegerField()),
                ('stream', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('roll_no', models.CharField(max_length=15, unique=True)),
                ('semester', models.IntegerField()),
                ('stream', models.CharField(max_length=40)),
                ('honor', models.CharField(max_length=10)),
                ('major', models.CharField(blank=True, max_length=30, null=True)),
                ('minor', models.CharField(blank=True, max_length=30, null=True)),
                ('exploratory', models.CharField(blank=True, max_length=30, null=True)),
                ('major_id', models.CharField(max_length=30)),
                ('minor_id', models.CharField(max_length=30)),
                ('exploratory_id', models.CharField(max_length=30)),
                ('batch', models.CharField(max_length=10)),
                ('course_duration', models.IntegerField()),
                ('contact_no', models.BigIntegerField()),
                ('personal_mail', models.EmailField(max_length=254)),
                ('parents_contact_no', models.BigIntegerField()),
                ('parents_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
