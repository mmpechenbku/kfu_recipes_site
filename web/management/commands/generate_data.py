from django.core.management import BaseCommand
from random import randint, choice
from web.models import Recipe, Ingredient, IngredientQuantity, RecipeStep, User


class Command(BaseCommand):
    def handle(self, *args, **options):

        user = User.objects.first()

        recipes = []

        ingredients = Ingredient.objects.all()

        for recipe_index in range(50):
            recipes.append(Recipe(
                title=f'generated {recipe_index}',
                description=f'generated recipe for analytics number {recipe_index}',
                difficulty=choice(('hard', 'medium', 'easy')),
                cooking_time=randint(1, 200),
                author=user,
                access='private',
            ))

        saved_recipes = Recipe.objects.bulk_create(recipes)

        recipe_ingredients = []
        steps = []
        ingredient_quantity = []

        for recipe in saved_recipes:
            count_of_ingredients = randint(1, len(ingredients))
            steps_count = randint(1, 10)
            for ingredient_index in range(count_of_ingredients):
                recipe_ingredients.append(
                    Recipe.ingredients.through(
                        recipe_id=recipe.id, ingredient_id=ingredients[ingredient_index].id
                    )
                )
                ingredient_quantity.append(IngredientQuantity(
                    recipe=recipe,
                    ingredient=ingredients[ingredient_index],
                    quantity=randint(1, 50)
                ))

            for step in range(steps_count):
                steps.append(RecipeStep(
                    recipe=recipe,
                    description=f'generated step for recipe "{recipe.title}"',
                    step_number=step
                ))

        Recipe.ingredients.through.objects.bulk_create(recipe_ingredients)
        IngredientQuantity.objects.bulk_create(ingredient_quantity)
        RecipeStep.objects.bulk_create(steps)
