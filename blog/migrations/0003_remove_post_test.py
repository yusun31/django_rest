# Generated by Django 3.1.13 on 2022-02-11 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='test',
        ),
    ]
