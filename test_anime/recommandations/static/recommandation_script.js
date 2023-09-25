function getAPIData(search_field){
    $.ajax({
        method: 'GET',
        url : "http://127.0.0.1:8000/api/list?search="+search_field,
        success: function(response) {
            putTableData(response);
        }
    })
}

function putTableData(response){
    var rows = "";
    var results = response.results;


    for (var i = 0; i < results.length; i += 3) {
        rows += "<div class='row_anime'>";
        for (var j = i; j < i + 3 && j < results.length; j++) {
            rows += "<div class='col_anime' data-id='"+results[j].id+"' data-title='"+results[j].title+"'>" + "<img src='"+ results[j].image +"' >"+results[j].title + "</div>";
        }
        rows += "</div>";
    }

    document.getElementById("display_result").innerHTML = "aaaa";
    $("#display_result").html(rows);

    $(".col_anime").on('click', function () {
        document.getElementById("anime_selection").style.visibility = "hidden";
        document.querySelector("#selector_choice").innerHTML = $(this).data("title");
        current_id = $(this).data("id");
        getRecommandations($(this).data("title"), $(this).data("id"));
    });
}

let current_id = 0;

function getRecommandations(title_anime, id){
    $.ajax({
        method: 'GET',
        url : "http://127.0.0.1:8000/api/get_recom",
        data: {
            id: id,
            title: title_anime,
            weight_themes: document.querySelector('select[name="theme"]').value,
            weight_studio: document.querySelector('select[name="studio"]').value,
            weight_genres: document.querySelector('select[name="genre"]').value,
            weight_summary: document.querySelector('select[name="summary"]').value,
        },
        success: function(response) {
            putTableDataRecom(response);
        }
    })
}

function putTableDataRecom(response){
    var rows = "";
    var results = response;

    for (var i = 0; i < results.length; i += 2) {
        rows += "<div class='row_anime_recom'>";
        for (var j = i; j < i + 2 && j < results.length; j++) {
            rows += "<div class='col_anime_recom' data-id='"+results[j].id+"' data-title='"+results[j].title+"'>" + + "<img src='"+ results[j].image +"' >"+ results[j].title + "</div>";
        }
        rows += "</div>";
    }
    $("#results_screen").html(rows);

}

document.querySelector('select[name="theme"]').addEventListener('change', handleSelectionChange);
document.querySelector('select[name="studio"]').addEventListener('change', handleSelectionChange);
document.querySelector('select[name="genre"]').addEventListener('change', handleSelectionChange);
document.querySelector('select[name="summary"]').addEventListener('change', handleSelectionChange);

function handleSelectionChange() {

    // Récupérez le contenu de l'élément #selector_choice correspondant à cet élément de sélection
    anime_selected = document.querySelector("#selector_choice").innerHTML;
    // Vérifiez si le contenu n'est pas vide et que la valeur sélectionnée a changé
    if (anime_selected !== "" ) {
        // Appelez la fonction getRecom() ou toute autre fonction que vous souhaitez
        getRecommandations(anime_selected, current_id);
    }
}


let searchTimer; // Variable pour stocker le timer

function delayedSearch(searchTerm) {
    // Annulez le timer précédent s'il existe
    clearTimeout(searchTimer);

    // Démarrez un nouveau timer pour déclencher la recherche après un délai (par exemple, 300 ms)
    searchTimer = setTimeout(function() {
        getAPIData(searchTerm);
    }, 300); // 300 ms de délai (ajustez selon vos besoins)
}

$("#input_search").on('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    delayedSearch(searchTerm);
});


document.getElementById('selector_choice').addEventListener('click', (e) => {
    e.stopPropagation(); // Empêche la propagation du clic à la fenêtre

    document.getElementById("anime_selection").style.visibility = "visible";
});

// Ajoutez l'écouteur d'événements click pour masquer la fenêtre à l'extérieur
window.addEventListener('click', function(e) {
    if (!document.getElementById('selection_window').contains(e.target)) {
        document.getElementById("anime_selection").style.visibility = "hidden";
    }
});






