# Generated by Django 3.0.8 on 2020-10-27 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_posts_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='uni',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
