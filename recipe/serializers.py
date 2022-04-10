from rest_framework import serializers

from recipe.models import Recipe

class SimpleRecipeSerializer(serializers.Serializer):
    ingredients = serializers.SerializerMethodField(method_name='parse_ingredients')
    numSteps = serializers.SerializerMethodField(method_name='calculate_steps')
    def parse_ingredients(self, recipe: Recipe):
        ingredients = recipe.ingredients.split("|")
        return ingredients
    def parse_instructions(self, recipe: Recipe):
        instructions = recipe.instructions.split("|")
        return instructions
    def calculate_steps(self, recipe: Recipe):
        instructions = self.parse_instructions(recipe)
        return len(instructions)

class DetailedRecipeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    ingredients = serializers.CharField(max_length=1024)
    instructions = serializers.CharField(max_length=1024)
    class Meta:
        model = Recipe
        fields = ["name", "ingredients", "instructions"]

    def create(self, data):
        recipe = Recipe(**data)
        recipe.save()
        return recipe

    def update(self, instance:Recipe, validated_data):
        instance.ingredients = validated_data["ingredients"]
        instance.instructions = validated_data["instructions"]
        instance.save()
        return instance

    def to_internal_value(self, data):
        data["ingredients"] = "|".join(data["ingredients"])
        data["instructions"] = "|".join(data["instructions"])
        return data