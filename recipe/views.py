from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from recipe.models import Recipe
from recipe.serializers import DetailedRecipeSerializer, SimpleRecipeSerializer

@api_view(['GET', 'PUT', 'POST'])
def recipe_names(request):
    print(request)
    if request.method == 'GET':
        recipe_names = Recipe.objects.values_list('name')
        recipe_names = list(map(lambda item: item[0], recipe_names))
        return Response({'recipeNames': recipe_names})
    elif request.method == 'PUT':
        target_recipe = Recipe.objects.filter(name = request.data.get('name')).first()   
        if target_recipe:
            serializer = DetailedRecipeSerializer(target_recipe, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({}, status=HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Recipe does not exist"}, status=HTTP_404_NOT_FOUND)
            
    elif request.method == 'POST':
        target_recipe = Recipe.objects.filter(name = request.data.get('name')).first()   
        if target_recipe:
            return Response({"error":"Recipe already exists"}, status=HTTP_400_BAD_REQUEST)
        else:
            serializer = DetailedRecipeSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({}, status=HTTP_201_CREATED)

@api_view(['GET'])
def recipe_detail(request, recipe_name):
    target_recipe = Recipe.objects.filter(name = recipe_name).first()
    if target_recipe:
        target_recipe = SimpleRecipeSerializer(target_recipe)
        return Response({"details":target_recipe.data})
    return Response({})
