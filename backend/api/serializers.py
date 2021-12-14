import base64
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Tag, Recipe, Ingredient, IngredientType, RecipeIngredients
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag"""

    class Meta:
        model = Tag
        fields = '__all__'


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
    id = serializers.PrimaryKeyRelatedField(queryset=IngredientType.objects.all(), source='type')
    class Meta:
        model = Ingredient
        exclude = ('type',)


class RecipeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeGetSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField(required=False, read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(required=False, read_only=True)
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientGetSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_is_favorite(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


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
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(**ingredient)
            RecipeIngredients.objects.create(ingredient=current_ingredient, recipe=recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tag_list = validated_data.pop('tags')
        Recipe.objects.filter(id=instance.id).update(**validated_data)
        instance.tags.set(tag_list)
        instance.ingredients.clear()
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(**ingredient)
            RecipeIngredients.objects.create(ingredient=current_ingredient, recipe=instance)
        instance.save()
        return instance

    class Meta:
        model = Recipe
        exclude = ('pub_date', 'author')
