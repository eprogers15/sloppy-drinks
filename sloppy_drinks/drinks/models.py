from django.db import models
from django.db.models import F, FloatField, ExpressionWrapper, Count, Q
from django.db.models.functions import Cast

# Create your models here.
class Ingredient(models.Model):
    """Model representing a drink ingredient"""
    name = models.CharField(max_length=100, primary_key=True, help_text='Enter an ingredient name (e.g. Simple Syrup)')
    filter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class RecipeSource(models.Model):
    """Model representing a recipe source"""
    name = models.CharField(max_length=100, primary_key=True)
    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Drink(models.Model):
    """Model representing a drink"""
    name = models.CharField(max_length=200, primary_key=True)
    slug = models.SlugField(default="", null=False)
    ingredients = models.ManyToManyField(Ingredient, help_text='Select the ingredients for this drink')
    recipe_source = models.ForeignKey(RecipeSource, blank=True, null=True, on_delete=models.PROTECT)
    recipe_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    # Return three Drink objects with highest similarity score sorted first descending by similarity_score and second ascending by name
    def get_similar_drinks(self):
        similar_drinks = Drink.objects.exclude(name=self.name).annotate(intersection_ingredients_count=Count('ingredients', filter=Q(ingredients__in=self.ingredients.all())), union_ingredients_count=Count('ingredients', distinct=True) + self.ingredients.count(), similarity_score=ExpressionWrapper(F('intersection_ingredients_count') / Cast(F('union_ingredients_count') - F('intersection_ingredients_count'), output_field=FloatField()), output_field=FloatField())).filter(similarity_score__gt=0.3).order_by('-similarity_score', 'name')[:3]
        return similar_drinks

class Episode(models.Model):
    """Model representing an Episode"""
    number = models.IntegerField(primary_key=True)
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True)
    date = models.DateField(unique=True)
    apple_podcasts_url = models.URLField(max_length=200, default='https://podcasts.apple.com/us/podcast/the-sloppy-boys/id1537187838')
    spotify_url = models.URLField(max_length=200, default='https://open.spotify.com/show/3qFjDCQ16YrjFw5ufNpV3c')
    youtube_url = models.URLField(max_length=200, blank=True, default='')
    instagram_post_url = models.URLField(max_length=200, blank=True, null=True)
    x_post_url = models.URLField(max_length=200, blank=True, null=True)
    bluesky_post_url = models.URLField(max_length=200, blank=True, null=True)

class ImageSource(models.Model):
    """Model representing an image source"""
    name = models.CharField(max_length=100, primary_key=True)
    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Image(models.Model):
    """Model representing an image"""
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)
    filename = models.CharField(max_length=240, primary_key=True)
    source = models.ForeignKey(ImageSource, on_delete=models.PROTECT)
    recipe = models.BooleanField(default=False)