from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

class Recipe(models.Model):

    class RecipeManager(models.Manager):
        def detail(self):
            return self.get_queryset() \
                 .prefetch_related('ingredients', 'likes', 'steps')

        def popular(self):
            return self.get_queryset() \
                .annotate(likes_count=Count('likes')) \
                .order_by('-likes_count')


    DIFFICULTY_OPTIONS = (
        ('hard', 'Сложный'),
        ('medium', 'Средней сложности'),
        ('easy', 'Легкий')
    )

    ACCESS_OPTIONS = (
        ('public', 'Общедоступный'),
        ('private', 'Закрытый')
    )

    picture = models.ImageField(upload_to='images/recipes_pictures', blank=True, null=True, verbose_name='Фото')
    title = models.CharField(max_length=255, verbose_name='Название')
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredients')
    description = models.TextField(verbose_name="Описание приготовления")
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_OPTIONS, verbose_name='Сложность')
    cooking_time = models.IntegerField(verbose_name="Время приготовления")
    author = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE)
    access = models.CharField(choices=ACCESS_OPTIONS, default='private', verbose_name='Доступ', max_length=10)

    objects = RecipeManager()

    @property
    def get_sum_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    quantity = models.CharField(max_length=50, verbose_name='Количество')

    def __str__(self):
        return f'{self.recipe.title} - {self.ingredient.name}: {self.quantity}'

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количества ингредиентов'


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='steps')
    image = models.ImageField(upload_to='images/recipes_pictures/steps', blank=True, null=True, verbose_name='Фото шага')
    description = models.TextField(max_length=3000, verbose_name='Описание шага')
    step_number = models.IntegerField(verbose_name='Номер шага')

    def __str__(self):
        return f'{self.recipe.title}, Шаг приготовления {self.step_number}'

    class Meta:
        verbose_name = 'Шаг приготовления'
        verbose_name_plural = 'Шаги приготовления'


class LikeRecipe(models.Model):
    recipe = models.ForeignKey(to=Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'