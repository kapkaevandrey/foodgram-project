from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (FavoriteRecipe, Ingredient, IngredientType, Recipe,
                     RecipeIngredient, RecipeTag, ShoppingList, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('slug',)
    list_filter = ('color',)


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type', 'amount')
    search_fields = ('type',)
    list_select_related = True


class IngredientInstance(admin.TabularInline):
    model = Ingredient


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    search_fields = ('recipe',)
    list_filter = ('tag',)
    list_select_related = True


@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient')
    search_fields = ('recipe',)
    list_filter = ('ingredient',)


@admin.register(FavoriteRecipe)
class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author',
                    'cooking_time', 'pub_date', 'favorites_num')
    search_fields = ('name', 'author')
    list_filter = ('tags', 'author')

    def favorites_num(self, obj):
        print(self)
        return obj.recipe_followers.count()

    favorites_num.short_description = _('Saved to favorite')
