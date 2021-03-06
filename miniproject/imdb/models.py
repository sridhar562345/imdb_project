from django.db import models
import datetime

class Director(models.Model):
    gender_choices = (
        ('male','female'),
        ('female','male'),
        ('other','other'),
    )
    name = models.CharField(max_length=100,unique=True)
    gender = models.CharField(max_length = 8,choices = gender_choices)
    fb_likes = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class Actor(models.Model):
    gender_choices = (
        ('male','female'),
        ('female','male'),
        ('other','other'),
    )
    actor_id = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    dob = models.DateField(null = True,blank = True)
    gender = models.CharField(max_length = 8,choices = gender_choices)
    fb_likes = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=100)
    movie_year = models.IntegerField() 
    box_office_collection_in_crores = models.FloatField()
    budget_in_crores = models.IntegerField()
    imdb_link = models.TextField()
    runtime_Minutes = models.IntegerField()
    genre = models.CharField(max_length = 100)
    average_rating = models.FloatField(max_length = 50)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors=models.ManyToManyField(Actor,
                            through='Cast',
                            through_fields=('movie','actor'))
    def __str__(self):
        return self.name


    
    
class Cast(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=50,null=True,blank = True)
    is_debut_movie = models.BooleanField(default = False)
    
    
    def __str__(self):
        return (self.actor.name+self.movie.name)
