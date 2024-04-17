# Generated by Django 4.2.11 on 2024-04-16 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvlog', '0007_alter_currentlywatching_episode_userex'),
    ]

    operations = [
        migrations.AddField(
            model_name='userex',
            name='watchlist',
            field=models.ManyToManyField(to='tvlog.show'),
        ),
        migrations.AlterField(
            model_name='show',
            name='boxart',
            field=models.ImageField(upload_to='images/'),
        ),
    ]