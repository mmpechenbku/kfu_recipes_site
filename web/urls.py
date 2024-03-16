from django.urls import path
from web.views import home_view, registration_view, auth_view, logout_view, add_recipe_view, IngredientSearchView, \
    recipes_view, RecipeDetailView, LikeRecipeView, analytics_view, import_view

urlpatterns = [
    path('', home_view, name='home'),
    path('sign_up/', registration_view, name='sign_up'),
    path("sign_in/", auth_view, name="sign_in"),
    path("sign_out/", logout_view, name="sign_out"),
    path("recipes/", recipes_view, name="recipes"),
    path('recipes/add_recipe/', add_recipe_view, name='add_recipe'),
    path('recipes/edit_recipe/<int:pk>/', add_recipe_view, name='edit_recipe'),
    path('recipes/api/ingredients/', IngredientSearchView.as_view(), name='ingredient-search'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/like_recipe/', LikeRecipeView.as_view(), name='like_recipe'),
    path('analytics/', analytics_view, name='analytics'),
    path("import/", import_view, name="import"),
]