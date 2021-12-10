from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    """Tag for recipe"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default='#42aaff')

    def __str__(self):
        return self.name


class IngredientType(models.Model):
    """Type of ingredient and unit of measurement """
    title = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} ({self.measurement_unit})"


class Ingredient(models.Model):
    """Description ingredient"""
    type = models.ForeignKey(IngredientType, on_delete=models.CASCADE,
                             related_name='ingredients')
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.type} - {self.quantity}"


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='recipe_ingredient', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"


class Recipe(models.Model):
    """Recipe of the dish"""
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='recipes/')
    tag = models.ManyToManyField(Tag, through='RecipeTag', blank=False)
    ingredient = models.ForeignKey(Ingredient, related_name='recipes', on_delete=models.CASCADE)
    pub_data = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.title} - {self.author.username}"


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='tag',  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag} - {self.recipe}"


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='following',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} follow to {self.author}"


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User, related_name='recipe_followers', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='favorite_recipes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} favorite recipe {self.recipe}"



