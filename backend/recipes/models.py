from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class Tag(models.Model):
    """Tag for recipe"""
    name = models.CharField(max_length=256, verbose_name=_('name'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    color = models.CharField(
        max_length=7,
        default='#42aaff',
        verbose_name=_('color'),
        validators=[RegexValidator(
            regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
            message=_(
                'The HEX code is not valid, please use the format #ffffff'
            ))]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class IngredientType(models.Model):
    """Type of ingredient and unit of measurement """
    name = models.CharField(_('name'),
                            max_length=256)
    measurement_unit = models.CharField(_('measurement_unit'), max_length=20)

    def __str__(self):
        return _('{title} ({mou})').format(title=self.name,
                                           mou=self.measurement_unit)

    class Meta:
        ordering = ['name']
        verbose_name = _('Type of ingredient')
        verbose_name_plural = _('Type of ingredient')
        constraints = [models.UniqueConstraint(
            fields=["name", "measurement_unit"], name="unique ingredient type"
        )]


class Ingredient(models.Model):
    """Description ingredient"""
    type = models.ForeignKey(IngredientType, on_delete=models.CASCADE,
                             related_name='ingredients')
    amount = models.FloatField(
        validators=(MinValueValidator(0.0),)
    )

    def __str__(self):
        return _('{type} - {amount}').format(type=self.type,
                                             amount=self.amount)

    class Meta:
        ordering = ['type']
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        constraints = [models.UniqueConstraint(
            fields=["type", "amount"], name="unique ingredient"
        )]


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey('Recipe',
                               related_name='recipe_ingredient',
                               on_delete=models.CASCADE,
                               verbose_name=_('recipe'))
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='ingredient_recipe',
                                   on_delete=models.CASCADE,
                                   verbose_name=_('ingredient'))

    def __str__(self):
        return _('{recipe} - {ingredient}').format(recipe=self.recipe,
                                                   ingredient=self.ingredient)

    class Meta:
        ordering = ['recipe']
        verbose_name = _('Recipe Ingredients')
        verbose_name_plural = _('Recipes Ingredients')
        constraints = [models.UniqueConstraint(
            fields=["recipe", "ingredient"],
            name="unique recipe ingredients")]


class Recipe(models.Model):
    """Recipe of the dish"""
    author = models.ForeignKey(User,
                               related_name='recipes',
                               on_delete=models.CASCADE,
                               verbose_name=_('author'))
    name = models.CharField(max_length=256, verbose_name=_('title'))
    text = models.TextField(verbose_name=_('description'))
    image = models.ImageField(upload_to='recipes/')
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    ingredients = models.ManyToManyField(Ingredient,
                                         through=RecipeIngredients)
    cooking_time = models.PositiveBigIntegerField(
        verbose_name=_('cooking time')
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name=_('date of publication'))
    recipe_followers = models.ManyToManyField(
        User,
        through='FavoriteRecipes',
        related_name='favorite_recipes',
        verbose_name=_('recipe subscribers')
    )
    shop_followers = models.ManyToManyField(
        User,
        through='ShoppingList',
        related_name='shopping_list',
        verbose_name=_('saved to the shopping list')
    )

    def __str__(self):
        return _('{title}').format(title=self.name)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe,
                               related_name='tag',
                               on_delete=models.CASCADE,
                               verbose_name=_('recipe'))
    tag = models.ForeignKey(Tag,
                            related_name='recipes',
                            on_delete=models.CASCADE,
                            verbose_name=_('tag'))

    def __str__(self):
        return _('{tag} - {recipe}').format(tag=self.tag, recipe=self.recipe)

    class Meta:
        ordering = ['recipe']
        verbose_name = _('Recipe Tag')
        verbose_name_plural = _('Recipes Tags')
        constraints = [models.UniqueConstraint(
            fields=["recipe", "tag"], name="unique recipe tag"
        )]


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )

    def __str__(self):
        return _('{user} - {recipe}').format(user=self.user,
                                             recipe=self.recipe)

    class Meta:
        ordering = ['user']
        verbose_name = _('Favorite Recipe')
        verbose_name_plural = _('Favorite Recipes')
        constraints = [models.UniqueConstraint(
            fields=["user", "recipe"], name="unique favorite user recipe"
        )]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe')
    )

    def __str__(self):
        return _('{user} - {recipe}').format(user=self.user,
                                             recipe=self.recipe)

    class Meta:
        ordering = ['user']
        verbose_name = _('Shopping List')
        verbose_name_plural = _('Shopping Lists')
        constraints = [models.UniqueConstraint(
            fields=["user", "recipe"], name="unique recipe in shopping list"
        )]
