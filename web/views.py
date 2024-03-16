from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from web.forms import RegistrationForm, AuthForm, RecipeFilterForm
from web.models import Ingredient, Recipe, IngredientQuantity, RecipeStep, LikeRecipe
from web.services import filter_recipes

User = get_user_model()

# def paginate(model, per_page=10):
#     paginator = Paginator(model, per_page)

def home_view(request):
    recipes = Recipe.objects.popular()
    likes = LikeRecipe.objects.filter(user=request.user).values_list('recipe',
                                                                     flat=True) if request.user.is_authenticated else None

    filter_form = RecipeFilterForm(request.GET)
    filter_form.is_valid()
    recipes = filter_recipes(recipes, filter_form.cleaned_data)

    total_count = recipes.count()

    paginator = Paginator(recipes, per_page=10)
    page_number = request.GET.get("page", 1)

    data = {
        'recipes': paginator.get_page(page_number),
        'likes': likes,
        'filter_form': filter_form,
        'total_count': total_count
    }
    return render(request, 'web/home.html', data)


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"]
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        'form': form,
        'is_success': is_success,
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("home")
    return render(request, "web/auth.html", {
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def add_recipe_view(request, pk=None):
    if request.method == 'POST':
        try:

            recipe_name = request.POST.get('recipe_name')
            recipe_description = request.POST.get('recipe_description')
            recipe_image = request.FILES.get('recipe_image')
            difficulty = request.POST.get('difficulty')
            cooking_time = request.POST.get('cooking_time')
            ingredient_ids = request.POST.get('ingredients', '').split(',')
            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)

            recipe = get_object_or_404(Recipe, author=request.user, id=pk) if pk is not None else None

            if recipe == None:
                recipe = Recipe.objects.create(
                    title=recipe_name,
                    description=recipe_description,
                    picture=recipe_image,
                    difficulty=difficulty,
                    cooking_time=cooking_time,
                    author=request.user,
                )
            else:
                Recipe.objects.filter(id=recipe.id).update(
                    title=recipe_name,
                    description=recipe_description,
                    picture=recipe_image,
                    difficulty=difficulty,
                    cooking_time=cooking_time,
                    author=request.user,
                )
            recipe.ingredients.set(ingredients)

            ingredient_quantity = IngredientQuantity.objects.filter(recipe=recipe)
            ingredient_quantity.delete()

            for ingredient in ingredients:
                quantity = request.POST.get(f'quantity_{ingredient.id}')

                IngredientQuantity.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )

            steps = RecipeStep.objects.filter(recipe=recipe)
            steps.delete()

            steps_count = int(request.POST.get('steps_count', 0))
            for i in range(1, steps_count + 1):
                step_description = request.POST.get(f'step_description_{i}')
                step_image = request.FILES.get(f'step_image_{i}')

                RecipeStep.objects.create(
                    recipe=recipe,
                    description=step_description,
                    image=step_image,
                    step_number=i
                )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        ingredients = Ingredient.objects.all()
        recipe = get_object_or_404(Recipe, author=request.user, id=pk) if pk is not None else None
        data = {
            'ingredients': ingredients,
        }
        if recipe != None:
            ingredients_in_recipe = []
            for ingredient in recipe.ingredients.all():
                ingredients_in_recipe.append(ingredient.name)
            quantity_ingr = IngredientQuantity.objects.filter(recipe=recipe)
            steps = RecipeStep.objects.filter(recipe=recipe).order_by('step_number')
            data['recipe'] = recipe
            data['ingredients_in_recipe'] = ingredients_in_recipe
            data['quantity_ingr'] = quantity_ingr
            data['steps'] = steps
            data['url'] = f'edit_recipe/{pk}/'
        else:
            data['url'] = 'add_recipe/'

        return render(request, 'web/add_recipe_test.html', data)


class IngredientSearchView(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        ingredients = Ingredient.objects.filter(name__icontains=search_query)
        data = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients]
        return JsonResponse(data, safe=False)


def recipes_view(request):
    recipes = Recipe.objects.all().order_by("title")
    likes = LikeRecipe.objects.filter(user=request.user).values_list('recipe',
                                                                     flat=True) if request.user.is_authenticated else None
    filter_form = RecipeFilterForm(request.GET)
    filter_form.is_valid()
    recipes = filter_recipes(recipes, filter_form.cleaned_data)

    total_count = recipes.count()

    paginator = Paginator(recipes, per_page=10)
    page_number = request.GET.get("page", 1)

    data = {
        'recipes': paginator.get_page(page_number),
        'likes': likes,
        'filter_form': filter_form,
        'total_count': total_count,
    }
    return render(request, 'web/recipes_list.html', data)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'web/recipe_detail.html'
    context_object_name = 'recipe'
    queryset = model.objects.detail()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title

        ingredients = []
        for ingredient in self.object.ingredients.all():
            ingredients.append(ingredient.name)

        context['ingredients'] = ingredients
        context['quantity_ingr'] = IngredientQuantity.objects.filter(recipe=self.object)
        context['likes'] = LikeRecipe.objects.filter(user=self.request.user).values_list('recipe',
                                                                                         flat=True) if self.request.user.is_authenticated else None
        context['steps'] = RecipeStep.objects.filter(recipe=self.object).order_by('step_number')
        return context


class LikeRecipeView(View, LoginRequiredMixin):
    model = LikeRecipe

    def post(self, request, *args, **kwargs):
        recipe_id = request.POST.get('recipe_id')
        user = request.user if request.user.is_authenticated else None
        if user:
            like, created = self.model.objects.get_or_create(
                recipe_id=recipe_id,
                user=user
            )
            count = str(like.recipe.get_sum_likes)
            if not created:
                like.delete()
                return JsonResponse({'status': 'deleted', 'likesSum': like.recipe.get_sum_likes})

            return JsonResponse({'status': 'created', 'likesSum': like.recipe.get_sum_likes})
