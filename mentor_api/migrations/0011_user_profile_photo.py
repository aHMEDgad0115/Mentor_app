# Generated by Django 4.2.2 on 2023-07-05 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor_api', '0010_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
