# Generated by Django 3.0.8 on 2020-12-01 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20201201_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='video',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
