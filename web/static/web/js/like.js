const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const csrftoken = getCookie("csrftoken");

const saveButton = document.querySelectorAll('.like-button');

saveButton.forEach(button => {
    button.addEventListener('click', event => {
        const recipeId = parseInt(button.dataset.recipe)
//        const saveSum = button.querySelector('.save-sum');
        const formData = new FormData();

        formData.append('recipe_id', recipeId);

        fetch("/recipes/like_recipe/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            if (data.status == 'created') {
                var style = 'border-color: #f44336; cursor: pointer;';
            } else {
                var style = 'cursor: pointer;';
            }
            button.style = style;
            button.innerText = "Likes: " + data.likesSum;
        })
        .catch(error => console.error(error));
    });
});