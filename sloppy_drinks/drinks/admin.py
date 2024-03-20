from django.contrib import admin
from django.contrib import admin
from drinks.models import *

# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    pass

class RecipeSourceAdmin(admin.ModelAdmin):
    pass

class DrinkAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class EpisodeAdmin(admin.ModelAdmin):
    pass

class ImageSourceAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeSource, RecipeSourceAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(ImageSource, ImageSourceAdmin)
admin.site.register(Image, ImageAdmin)