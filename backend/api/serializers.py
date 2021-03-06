import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Ingredient, IngredientType, Recipe,
                            RecipeIngredient, Tag)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        required=False,
        read_only=True
    )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.users.filter(author=obj).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('username', 'email')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate_color(self, value):
        if not re.fullmatch(settings.HEX_PATTERN, value):
            raise serializers.ValidationError(
                _('The HEX code is not valid, please use the format #ffffff'))
        return value


class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = '__all__'


class IngredientGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='type.name')
    measurement_unit = serializers.CharField(source='type.measurement_unit')

    class Meta:
        model = Ingredient
        exclude = ('type',)


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=IngredientType.objects.all(),
        source='type')

    class Meta:
        model = Ingredient
        exclude = ('type',)


class RecipeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeGetSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField(
        required=False,
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        required=False,
        read_only=True
    )
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientGetSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ('pub_date', 'recipe_followers', 'shop_followers')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.recipe_followers.filter(
            favoriterecipe__user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.shop_followers.filter(
            shoppinglist__user=user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        required=True,
        many=True
    )
    ingredients = IngredientSerializer(
        required=True,
        many=True)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tag_list = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tag_list)
        recipe = RecipeSerializer.get_and_update_instance(
            instance=recipe,
            ingredients=ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tag_list = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredients.clear()
        instance.tags.set(tag_list)
        instance = RecipeSerializer.get_and_update_instance(
            instance=instance,
            ingredients=ingredients
        )
        instance.save()
        return instance

    @staticmethod
    def get_and_update_instance(instance: Recipe,
                                ingredients: dict) -> Recipe:
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                type=ingredient['type'],
                amount=ingredient['amount']
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance
            )
        return instance

    def validate_ingredients(self, value):
        ingredients_type = [ingredient['type'] for ingredient in value]
        if len(ingredients_type) != len(set(ingredients_type)):
            raise serializers.ValidationError(
                _('This recipe already has this ingredient'))
        return value

    class Meta:
        model = Recipe
        exclude = ('pub_date', 'author', 'recipe_followers', 'shop_followers')


class GetUserSerializer(CustomUserSerializer):
    recipes = RecipeSimpleSerializer(many=True)
    recipes_count = serializers.SerializerMethodField(
        required=False,
        read_only=True
    )

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('username', 'email')
