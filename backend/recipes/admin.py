from django.contrib import admin

from .models import (Tag, IngredientType, Ingredient,
                     RecipeTag, Recipe, FavoriteRecipes)


admin.site.register(Tag)
admin.site.register(IngredientType)
admin.site.register(Ingredient)
admin.site.register(RecipeTag)
admin.site.register(Recipe)
admin.site.register(FavoriteRecipes)

