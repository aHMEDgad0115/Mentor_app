# Generated by Django 4.2.2 on 2023-07-05 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor_api', '0011_user_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='price',
            field=models.IntegerField(blank=True, default=100, max_length=5),
        ),
        migrations.AddField(
            model_name='user',
            name='cash',
            field=models.IntegerField(blank=True, default=10000, max_length=10),
        ),
    ]
