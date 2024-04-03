from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
# Create your models here.
class Show(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    boxart = models.ImageField(blank=True, null=True, upload_to="images/")
    abbreviation = models.SlugField()
    creation_date = models.DateField(auto_now_add=True,)

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50) # Seasons could have weird names. Even if most shows will just be a number, having support for something like "specials" would be valuable.
    episodes = models.PositiveSmallIntegerField()
    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    startdate = models.DateField()

    def __str__(self):
        return f"{self.show.name} - Season {self.name} ({self.episodes})"

class CurrentlyWatching(models.Model):
    author = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    episode = models.PositiveSmallIntegerField() # Referencing Season total episode count doesn't work, must be checked before added to database.
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)]) # 0 = No rating.
    rewatch = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author.username} watching {str(self.season)} on episode {self.episode}"

# class Watched(models.Model):
#     author = models.ForeignKey("auth.user", on_delete=models.CASCADE)
#     show = models.ForeignKey("Show", on_delete=models.CASCADE)
#     date = models.DateField(default=date.today)
#     review = models.CharField(max_length=500)
#     rewatch = models.BooleanField(default=False)
