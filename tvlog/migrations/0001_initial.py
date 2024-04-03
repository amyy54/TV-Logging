# Generated by Django 4.2.11 on 2024-04-01 14:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('episodes', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField(blank=True, null=True)),
                ('boxart', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('abbreviation', models.CharField(max_length=25, unique=True)),
                ('seasons', models.ManyToManyField(to='tvlog.season')),
            ],
        ),
        migrations.CreateModel(
            name='Watched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('rating', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('review', models.CharField(max_length=500)),
                ('rewatch', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvlog.show')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentlyWatching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('episode', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvlog.season')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvlog.show')),
            ],
        ),
    ]