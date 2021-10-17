# Generated by Django 3.0.8 on 2020-10-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_posts_uni'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='uni',
            field=models.CharField(blank=True, choices=[('KFUPM', 'KFUPM'), ('Harvard', 'Harvard'), ('Yale', 'Yale'), ('MIT', 'MIT'), ('Cambridge', 'Cambridge')], max_length=64),
        ),
        migrations.AlterField(
            model_name='posts',
            name='subject',
            field=models.CharField(blank=True, choices=[('Math', 'Math'), ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('English', 'English'), ('Biology', 'Biology'), ('Physical Education', 'Physical Education'), ('Business', 'Business'), ('Economics', 'Economics')], max_length=64),
        ),
    ]