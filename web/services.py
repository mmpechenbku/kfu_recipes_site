import csv
from web.models import Recipe, Ingredient
from recipes_site.redis import get_redis_client

def filter_recipes(recipes_qs, filters):
    if filters['search']:
        recipes_qs = recipes_qs.filter(title__icontains=filters['search'])

    if filters['difficulty']:
        recipes_qs = recipes_qs.filter(difficulty=filters['difficulty'])

    if filters['cooking_time']:
        recipes_qs = recipes_qs.filter(cooking_time__lte=filters['cooking_time'])

    return recipes_qs

def export_recipes_csv(recipes_qs, response):
    writer = csv.writer(response)
    writer.writerow(("title", "ingredients", "description", "difficulty", "cooking_time", "author",))

    for recipe in recipes_qs:
        writer.writerow((
            recipe.title,
            " ".join([ingr.name for ingr in recipe.ingredients.all()]),
            recipe.description, recipe.difficulty, recipe.cooking_time, recipe.author
        ))
    return response

def import_recipes_from_csv(file, user_id):
    strs_from_file = (row.decode() for row in file)
    reader = csv.DictReader(strs_from_file)

    recipes = []
    recipe_ingredients = []
    for row in reader:
        recipes.append(Recipe(
            title=row['title'],
            description=row['description'],
            difficulty=row['difficulty'],
            cooking_time=row['cooking_time'],
            author_id=user_id,
        ))

        recipe_ingredients.append(row['ingredients'].split(" ") if row['ingredients'] else [])

        ingredients_map = dict(Ingredient.objects.all().values_list('name', 'id'))
    saved_recipes = Recipe.objects.bulk_create(recipes)

    ingredients_in_recipes = []

    for recipe, ingredients_item in zip(saved_recipes, recipe_ingredients):
        for ingredient in ingredients_item:
            ingredient_id = ingredients_map[ingredient]
            ingredients_in_recipes.append(
                Recipe.ingredients.through(recipe_id=recipe.id, ingredient_id=ingredient_id)
            )
    Recipe.ingredients.through.objects.bulk_create(ingredients_in_recipes)

def get_stat():
    redis = get_redis_client()
    keys = redis.keys("stat_*")
    return [
        (key.decode().replace("stat_", ""), redis.get(key).decode())
        for key in keys
    ]
