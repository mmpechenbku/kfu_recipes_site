document.addEventListener('DOMContentLoaded', function () {

    var ingredientSelect = document.getElementById('id_ingredients');
    var quantityTBody = document.getElementById('ingredientquantity_set-group').querySelector('tbody');
    var addRow = quantityTBody.querySelector('.add-row');
    var ingredientCounter = 0;

    ingredientSelect.addEventListener('change', function () {
        var selectedIngredients = [];
        for (var i = 0; i < ingredientSelect.options.length; i++) {
            if (ingredientSelect.options[i].selected) {
                selectedIngredients.push({
                    value: ingredientSelect.options[i].value,
                    text: ingredientSelect.options[i].text
                });
            }
        }

        if (selectedIngredients.length > 0) {
            quantityTBody.style.display = 'table-row-group';
        } else {
            quantityTBody.style.display = 'none';
        }

        while (quantityTBody.firstChild) {
            quantityTBody.removeChild(quantityTBody.firstChild);
        }

        for (var j = 0; j < selectedIngredients.length; j++) {
            addIngredientRow(selectedIngredients[j].value, selectedIngredients[j].text);
        }
    });


    function addIngredientRow(ingredientValue, ingredientText) {
        var newRow = quantityTBody.insertRow();
        var originalTd = newRow.insertCell(0);
        var origTd = document.createElement('td');
        origTd.className = 'original';
        originalTd.appendChild(origTd);

        var cellIngredient = newRow.insertCell(1);
        var ingredientSelectCell = document.createElement('select');
        ingredientSelectCell.name = 'ingredientquantity_set-' + ingredientCounter + '-ingredient';
        ingredientSelectCell.id = 'id_ingredientquantity_set-' + ingredientCounter + '-ingredient';

        for (var k = 0; k < ingredientSelect.options.length; k++) {
                var option = document.createElement('option');
                option.value = ingredientSelect.options[k].value;
                option.text = ingredientSelect.options[k].text;
                if (ingredientSelect.options[k].selected){
                    option.disabled = true;
                }
                ingredientSelectCell.add(option);
        }

        ingredientSelectCell.addEventListener('change', function() {
            ingredientValue = ingredientSelectCell.value;
            var ingredientSelects = document.querySelectorAll('[id^="id_ingredientquantity_set-"][id$="-ingredient"]');
            var selected = [];
            ingredientSelects.forEach(function (select){
                for (var k = 0; k < ingredientSelect.options.length; k++) {
                   if (select.options[k].selected) {
                        selected.push(select.options[k])
                    }
                }
            })
            for (var k = 0; k < ingredientSelect.options.length; k++) {
                ingredientSelect.options[k].selected = false;
            }

            for (var k = 0; k < ingredientSelect.options.length; k++) {
                for (var j = 0; j < selected.length; j++) {
                    if (ingredientSelect.options[k].value == selected[j].value){
                        ingredientSelect.options[k].selected = true;
                        break;
                    }
                }
            }
            ingredientSelects.forEach(function (select) {
                for (var k = 0; k < ingredientSelect.options.length; k++) {
                    if (ingredientSelect.options[k].selected) {
                        select.options[k].disabled = true;
                    } else {
                        select.options[k].disabled = false;
                    }
                }
            })
        });

        ingredientSelectCell.value = ingredientValue;

        cellIngredient.appendChild(ingredientSelectCell);

        var changeLink = createLink('change', ingredientCounter, ingredientValue);
        cellIngredient.appendChild(changeLink);

        var addLink = createLink('add', ingredientCounter, ingredientValue);
        cellIngredient.appendChild(addLink);

        var viewLink = createLink('view', ingredientCounter, ingredientValue);
        cellIngredient.appendChild(viewLink);

        ingredientSelectCell.addEventListener('change', function() {
            changeLink.href = '/admin/recipes/ingredient/' + ingredientSelectCell.value + '/change/?_to_field=id&_popup=1';
            viewLink.href = '/admin/recipes/ingredient/' + ingredientSelectCell.value + '/change/?_to_field=id';
        });

        var cellQuantity = newRow.insertCell(2);
        var quantityInput = document.createElement('input');
        quantityInput.type = 'text';
        quantityInput.name = 'ingredientquantity_set-' + ingredientCounter + '-quantity';
        quantityInput.id = 'id_ingredientquantity_set-' + ingredientCounter + '-quantity';
        quantityInput.className = 'vTextField';
        cellQuantity.appendChild(quantityInput);

        var cellDelete = newRow.insertCell(3);
        var deleteLink = document.createElement('a');
        deleteLink.textContent = 'Удалить';
        deleteLink.className = 'inline-deletelink';
        deleteLink.href = '#';
        deleteLink.addEventListener('click', function (event) {

            var ingredientSelects = document.querySelectorAll('[id^="id_ingredientquantity_set-"][id$="-ingredient"]');

            event.preventDefault();
            quantityTBody.removeChild(newRow);
            for (var i = 0; i < ingredientSelect.options.length; i++) {
                if (ingredientSelect.options[i].value === ingredientValue) {
                    console.log(ingredientValue);
                    ingredientSelect.options[i].selected = false;
                    ingredientSelects.forEach(function (select) {
                        select.options[i].disabled = false;
                    });
                    break;
                }
            }
        });
        cellDelete.appendChild(deleteLink);
        ingredientCounter++;
    }

    function createLink(type, counter, ingredientValue) {
        var link = document.createElement('a');
        link.className = 'related-widget-wrapper-link ' + type + '-related';
        link.id = type + '_id_ingredientquantity_set-' + counter + '-ingredient';
        link.href = '/admin/recipes/ingredient/' + ingredientValue + '/' + type + '/?_to_field=id&_popup=1';
        link.title = getTitle(type);
        link.setAttribute('data-popup', 'yes');
        var img = document.createElement('img');
        img.src = '/static/admin/img/icon-' + type + 'link.svg';
        img.alt = getTitle(type);
        link.appendChild(img);
        return link;
    }

    function getTitle(type) {
        switch (type) {
            case 'change':
                return 'Изменить выбранный объект типа "Ингредиент"';
            case 'add':
                return 'Добавить ещё один объект типа "Ингредиент"';
            case 'view':
                return 'Просмотреть выбранный объект типа "Ингредиент"';
            default:
                return '';
        }
    }

});
