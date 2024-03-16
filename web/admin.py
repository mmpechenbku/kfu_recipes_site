from django.contrib import admin
from web.models import *


class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 0

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'difficulty', 'cooking_time', 'author')
    search_fields = ('id', 'title')
    list_filter = ('difficulty', 'cooking_time', 'author')
    inlines = [IngredientQuantityInline, RecipeStepInline]

    class Media:
        js = ('web/js/admin.js',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeStep)
admin.site.register(LikeRecipe)
admin.site.register(IngredientQuantity)
