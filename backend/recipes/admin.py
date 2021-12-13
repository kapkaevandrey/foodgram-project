from django.contrib import admin

from .models import (Tag, IngredientType, Ingredient,
                     RecipeTag, Recipe, FavoriteRecipes,
                     RecipeIngredients)


admin.site.register(Tag)
admin.site.register(IngredientType)
admin.site.register(Ingredient)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredients)
admin.site.register(Recipe)
admin.site.register(FavoriteRecipes)

