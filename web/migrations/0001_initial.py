# Generated by Django 5.0.3 on 2024-03-07 17:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images/recipes_pictures', verbose_name='Фото')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание приготовления')),
                ('difficulty', models.CharField(choices=[('hard', 'Сложный'), ('medium', 'Средней сложности'), ('easy', 'Легкий')], max_length=50, verbose_name='Сложность')),
                ('cooking_time', models.IntegerField(verbose_name='Время приготовления')),
                ('access', models.CharField(choices=[('public', 'Общедоступный'), ('private', 'Закрытый')], default='private', max_length=10, verbose_name='Доступ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('ingredients', models.ManyToManyField(related_name='ingredients', to='web.ingredient')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='IngredientQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=50, verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количества ингредиентов',
            },
        ),
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/recipes_pictures/steps', verbose_name='Фото шага')),
                ('description', models.TextField(max_length=3000, verbose_name='Описание шага')),
                ('step_number', models.IntegerField(verbose_name='Номер шага')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='web.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Шаг приготовления',
                'verbose_name_plural': 'Шаги приготовления',
            },
        ),
        migrations.CreateModel(
            name='LikeRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving', to='web.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'ordering': ('-time_create',),
                'indexes': [models.Index(fields=['-time_create'], name='web_likerec_time_cr_c9b608_idx')],
                'unique_together': {('recipe', 'user')},
            },
        ),
    ]
