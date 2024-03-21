from django.contrib import admin
from django.contrib import admin
from drinks.models import *

# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    ordering = ['name']

class RecipeSourceAdmin(admin.ModelAdmin):
    pass

class DrinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'recipe_url', 'recipe_source']
    list_filter = ('ingredients',)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ['name']

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'date', 'drink', 'apple_podcasts_url', 'spotify_url', 'instagram_post_url', 'x_post_url']
    ordering = ['number']

class ImageSourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['drink', 'filename', 'source', 'recipe']
    ordering = ['drink']

# Register your models here.
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeSource, RecipeSourceAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(ImageSource, ImageSourceAdmin)
admin.site.register(Image, ImageAdmin)