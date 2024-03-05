let container = document.getElementById('recipe_container')

fetch("http://localhost:3001/").then((Response) => {
        return Response.json()
    }).then((data) => {
        for (let index = 0; index < data.length; index++) {
            data[index] = 'q=' + data[index] + '&';
            
        }
        console.log(data.join(''));

        fetch("http://localhost:80/list/?" + data.join('')).then((Response) => {
                return Response.json()
            }).then((data) => {
                console.log(data);
                data.forEach(element => {
                    container.innerHTML +='<h2 id="recipe_name" class="title">' + element["title"] + '</h2>' +
                    '<img id="recipe_image" class="image" src="' + element["image"] + '" alt=" ">' +
                    '<p id="sourceLink" class="sourceUrl">' + element["sourceUrl"] + '</p>'
                });
            });
    })