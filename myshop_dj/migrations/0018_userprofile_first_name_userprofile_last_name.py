# Generated by Django 4.2.16 on 2024-12-17 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop_dj', '0017_userprofile_date_of_birth_userprofile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
