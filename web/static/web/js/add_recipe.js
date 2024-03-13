const availableIngredientsContainer = document.querySelector(
  ".available-ingredients"
);
const quantityIngredientsContainer = document.querySelector(
  ".ingredient-quantity"
);
const selectedIngredientIds = new Set();
const recipeForm = document.getElementById("recipe-form");

const ingredientsOnEdit = document.querySelectorAll(".ingr_edit");

if (ingredientsOnEdit.length != 0) {
    var ingredientId;
    for (var i = 0; i < ingredientsOnEdit.length; i++) {
        ingredientId = ingredientsOnEdit[i].getAttribute("data-ingredient-id");
        selectedIngredientIds.add(ingredientId);
    }
    const ingredientsOnPage = document.querySelectorAll(".ingredients-on-page");
    for (var i = 0; i < ingredientsOnPage.length; i++) {
        ingredientId = ingredientsOnPage[i].getAttribute("data-ingredient-id");
        if (selectedIngredientIds.has(ingredientId)) {
            ingredientsOnPage[i].disabled = true;
        }
    }
}

var ingredientCount = ingredientsOnEdit.length;
console.log(ingredientCount);

const stepsOnPage = document.querySelectorAll(".step");

var stepCount = stepsOnPage.length;
var maxSteps = 10;

availableIngredientsContainer.addEventListener("click", (event) => {
  const targetButton = event.target;
  if (targetButton.classList.contains("ingredient-button")) {
    const ingredientId = targetButton.getAttribute("data-ingredient-id");

    if (!selectedIngredientIds.has(ingredientId)) {
      selectedIngredientIds.add(ingredientId);
      const selectedIngredientButton = document.createElement("button");
      selectedIngredientButton.type = "button";
      selectedIngredientButton.className = "ingredient-button selected";
      selectedIngredientButton.setAttribute("data-ingredient-id", ingredientId);
      selectedIngredientButton.textContent = targetButton.textContent;
      quantityIngredientsContainer.appendChild(selectedIngredientButton);
      var div = document.createElement("div");
      div.innerHTML =
        '<input data-quantity="' +
        selectedIngredientButton.getAttribute("data-ingredient-id") +
        '" name="quantity_' +
        selectedIngredientButton.getAttribute("data-ingredient-id") +
        '" placeholder="Количество"></div>';
      quantityIngredientsContainer.appendChild(div);
      ingredientCount++;
    }

    targetButton.disabled = true;
    targetButton.style.display = "none";
  }
});

document.getElementById("add-step").addEventListener("click", function () {
  if (stepCount < maxSteps) {
    stepCount++;

    var stepsSection = document.getElementById("steps-section");
    var addedSteps = document.getElementById("added-steps");
    var div = document.createElement("div");
    var currentStep = stepCount;
    div.innerHTML =
      '<input type="file" name="step_image_' +
      stepCount +
      '" accept=".png, .jpg, .jpeg" id="step-image-' +
      currentStep +
      '">' +
      '<textarea name="step_description_' +
      stepCount +
      '" placeholder="Описание шага"  id="step-description-' +
      stepCount +
      '"></textarea>';

    addedSteps.appendChild(div);

    if (stepCount === maxSteps) {
      document.getElementById("add-step").style.display = "none";
    }
  }
  document
    .getElementById("step-description-" + currentStep)
    .addEventListener("input", function () {
      updateSummary();
    });
});

function updateSummary() {
  var summaryList = document.getElementById("summary-list");
  summaryList.innerHTML = "";

  for (var i = 0; i < stepCount; i++) {
    var stepDescription = document.getElementById(
      "step-description-" + (i + 1)
    ).value;

    var listItem = document.createElement("li");
    listItem.textContent = stepDescription;

    summaryList.appendChild(listItem);
  }
}

quantityIngredientsContainer.addEventListener("click", (event) => {
  const targetButton = event.target;
  if (targetButton.classList.contains("ingredient-button")) {
    const ingredientId = targetButton.getAttribute("data-ingredient-id");

    var quantityField = document.querySelector(
      '[name="quantity_' + ingredientId + '"]'
    );
    quantityField.remove();
    selectedIngredientIds.delete(ingredientId);

    targetButton.remove();

    const correspondingAvailableButton = document.querySelector(
      `.available-ingredients .ingredient-button[data-ingredient-id="${ingredientId}"]`
    );
    if (correspondingAvailableButton) {
      correspondingAvailableButton.disabled = false;
      correspondingAvailableButton.style.display = "unset";
    }
  }
});

document.getElementById("save-recipe").addEventListener("click", function () {
  const selectedIngredientIdsArray = Array.from(selectedIngredientIds);
  const selectedIngredientIdsString = selectedIngredientIdsArray.join(",");

  const hiddenInput = document.createElement("input");
  hiddenInput.type = "hidden";
  hiddenInput.name = "ingredients";
  hiddenInput.value = selectedIngredientIdsString;
  recipeForm.appendChild(hiddenInput);

  var formData = new FormData(document.getElementById("recipe-form"));

  formData.append("ingredients_count", ingredientCount);

  formData.append("steps_count", stepCount);

  url = document.getElementById("save-recipe").getAttribute("data-url");

  fetch("/recipes/" + url, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        alert("Рецепт успешно сохранен!");
        document.location.href = link;
      } else {
        alert("Произошла ошибка при сохранении рецепта.");
        console.log(data.message);
      }
    })
    .catch((error) => {
      console.error("Ошибка при отправке данных на сервер:", error);
    });
});

const ingredientSearchInput = document.getElementById("ingredient-search");
const ingredientButtonsContainer =
  document.getElementById("ingredient-buttons");

ingredientSearchInput.addEventListener("input", () => {
  ingredientButtonsContainer.innerHTML = '';
  const searchQuery = (
    ingredientSearchInput.value.charAt(0).toUpperCase() +
    ingredientSearchInput.value.slice(1).toLowerCase()
  ).trim();


  if (searchQuery.length >= 2) {
    fetch(`/recipes/api/ingredients/?search=${searchQuery}`)
      .then((response) => response.json())
      .then((data) => {
      ingredientButtonsContainer.innerHTML = '';
        data.forEach((ingredient) => {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "ingredient-button";
          button.setAttribute("data-ingredient-id", ingredient.id);
          button.textContent = ingredient.name;
          ingredientButtonsContainer.appendChild(button);

          const ingredientId = button.getAttribute("data-ingredient-id");
          if (selectedIngredientIds.has(ingredientId)) {
            button.disabled = true;
          }
        });
      });
  }
});
ingredientButtonsContainer.addEventListener("click", (event) => {
  const targetButton = event.target;
  ingredientButtonsContainer.innerHTML = "";

  if (targetButton.classList.contains("ingredient-button")) {
    const ingredientId = targetButton.getAttribute("data-ingredient-id");

    if (!selectedIngredientIds.has(ingredientId)) {
      selectedIngredientIds.add(ingredientId);

      const selectedIngredientButton = document.createElement("button");
      selectedIngredientButton.type = "button";
      selectedIngredientButton.className = "ingredient-button selected";
      selectedIngredientButton.setAttribute("data-ingredient-id", ingredientId);
      selectedIngredientButton.textContent = targetButton.textContent;

      quantityIngredientsContainer.appendChild(selectedIngredientButton);

      var div = document.createElement("div");
      div.innerHTML =
        '<input data-quantity="' +
        selectedIngredientButton.getAttribute("data-ingredient-id") +
        '" name="quantity_' +
        selectedIngredientButton.getAttribute("data-ingredient-id") +
        '" placeholder="Количество"></div>';
      quantityIngredientsContainer.appendChild(div);
      ingredientCount++;

      const correspondingAvailableButton = document.querySelector(
        `.available-ingredients .ingredient-button[data-ingredient-id="${ingredientId}"]`
      );
      correspondingAvailableButton.disabled = true;
      ingredientSearchInput.value = "";

      checkbox.disabled = false;
    }

    targetButton.disabled = true;
  }
});
