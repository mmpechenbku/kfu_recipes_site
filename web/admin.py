from django.contrib import admin
from web.models import *

class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 0

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientQuantityInline, RecipeStepInline]

    class Media:
        js = ('web/js/admin.js',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeStep)
admin.site.register(LikeRecipe)
admin.site.register(IngredientQuantity)
