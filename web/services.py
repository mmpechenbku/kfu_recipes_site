def filter_recipes(recipes_qs, filters):
    if filters['search']:
        recipes_qs = recipes_qs.filter(title__icontains=filters['search'])

    if filters['difficulty']:
        recipes_qs = recipes_qs.filter(difficulty=filters['difficulty'])

    if filters['cooking_time']:
        recipes_qs = recipes_qs.filter(cooking_time__lte=filters['cooking_time'])

    return recipes_qs
