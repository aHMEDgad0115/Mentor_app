# Generated by Django 4.2.2 on 2023-06-19 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='Bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
