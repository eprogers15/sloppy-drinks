from django.db import models

# Create your models here.
class Ingredient(models.Model):
    """Model representing a drink ingredient"""
    name = models.CharField(max_length=100, primary_key=True, help_text='Enter an ingredient name (e.g. Simple Syrup)')

class RecipeSource(models.Model):
    """Model representing a recipe source"""
    name = models.CharField(max_length=100, primary_key=True)
    url = models.URLField(max_length=200, blank=True, null=True)

class Drink(models.Model):
    """Model representing a drink"""
    name = models.CharField(max_length=200, primary_key=True)
    slug = models.SlugField(default="", null=False)
    ingredients = models.ManyToManyField(Ingredient, help_text='Select the ingredients for this drink')
    recipe_source = models.ForeignKey(RecipeSource, blank=True, null=True, on_delete=models.PROTECT)
    recipe_url = models.URLField(max_length=200, blank=True, null=True)

class Episode(models.Model):
    """Model representing an Episode"""
    number = models.IntegerField(primary_key=True)
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True)
    date = models.DateField(unique=True)
    acast_url = models.URLField(max_length=200, default='https://play.acast.com/s/thesloppyboys/')
    spotify_url = models.URLField(max_length=200, default='https://open.spotify.com/show/3qFjDCQ16YrjFw5ufNpV3c?si=4202cac534494845')
    instagram_post_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_post_url = models.URLField(max_length=200, blank=True, null=True)

class ImageSource(models.Model):
    """Model representing an image source"""
    name = models.CharField(max_length=100, primary_key=True)

class Image(models.Model):
    """Model representing an image"""
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)
    filename = models.CharField(max_length=240, primary_key=True)
    source = models.ForeignKey(ImageSource, on_delete=models.PROTECT)
    recipe = models.BooleanField(default=False)