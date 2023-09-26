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
            rows += "<div class='col_anime' data-id='"+results[j].id+"'>" +"<img src='"+results[j].image +"'>"+ results[j].title + "</div>";
        }
        rows += "</div>";
    }

    $("#display_result").html(rows);

    $(".col_anime").on('click', function () {
        var animeId = $(this).data("id");
        window.location.href = "/anime/" + animeId;
    });
}
let searchTimer; // Variable pour stocker le timer
function delayedSearch(searchTerm) {
    // Annulez le timer précédent s'il existe
    clearTimeout(searchTimer);

    // Démarrez un nouveau timer pour déclencher la recherche après un délai (par exemple, 300 ms)
    searchTimer = setTimeout(function() {
        getAPIData(searchTerm);
    }, 500); // 300 ms de délai (ajustez selon vos besoins)
}

$("#input_search").on('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    delayedSearch(searchTerm);
});