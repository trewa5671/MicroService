let btn = document.getElementById('gen_btn');
let recipe_name = document.getElementById('recipe_name');
let recipe_image = document.getElementById('recipe_image');
let servings = document.getElementById('servings');
let readyInMinutes = document.getElementById('readyInMinutes');
let healthScore = document.getElementById('healthScore');
let dishTypes = document.getElementById('dishTypes');
let sourceLink = document.getElementById('sourceLink');

let current = 0;

btn.onclick = async function() {
    fetch("http://localhost:80/").then((Response) => {
        return Response.json();
    }).then((data) => {
        current = data["id"]
        recipe_name.textContent = data["title"];
        recipe_image.src = data['image'];
        servings.textContent = "Количество порций: " + data['servings'];
        readyInMinutes.textContent = "Время приготовления (минуты): " + data['readyInMinutes'];
        healthScore.textContent = "Оценка здоровья: " + data['healthScore'];
        dishTypes.textContent = "Тип блюда: " + data['dishTypes'].join(', ');
        sourceLink.href = data['sourceUrl'];
        sourceLink.textContent = "Ссылка на рецепт";
    });
};

add = document.getElementById('add')

add.onclick = async function(){

    fetch("http://localhost:3001/?id=" + current.toString(), {
    method: "POST"
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
}