# Generated by Django 4.2.11 on 2024-04-24 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_corestreams'),
    ]

    operations = [
        migrations.CreateModel(
            name='response_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('sap_id', models.CharField(max_length=25)),
                ('total_correct', models.IntegerField()),
                ('total_incorrect', models.IntegerField()),
            ],
        ),
    ]
