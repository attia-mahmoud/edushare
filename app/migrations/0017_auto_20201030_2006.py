# Generated by Django 3.0.8 on 2020-10-30 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_posts_university'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
        migrations.DeleteModel(
            name='Posts',
        ),
    ]
