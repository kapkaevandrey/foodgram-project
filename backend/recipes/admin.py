from django.contrib import admin

from .models import (Tag, IngredientType, Ingredient,
                     RecipeTag, Recipe, FavoriteRecipes,
                     RecipeIngredients, ShoppingList)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('slug',)
    list_filter = ('color',)


class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type', 'amount')
    search_fields = ('type',)
    list_select_related = True


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    search_fields = ('recipe',)
    list_filter = ('tag',)
    list_select_related = True


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient')
    search_fields = ('recipe',)
    list_filter = ('ingredient',)


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'cooking_time', 'pub_date')
    search_fields = ('name', 'author')
    list_filter = ('tags', 'author')


admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientType, IngredientTypeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Recipe, RecipeAdmin)
