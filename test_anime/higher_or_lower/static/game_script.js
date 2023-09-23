
var anime1;
var anime2;

function getNewFreshAnime(){
    $.ajax({
        method: 'GET',
        url : 'http://127.0.0.1:8000/api/random?samples=2',
        success: function(response) {
            anime1 = response[0];
            anime2 = response[1];
            updateTitleContents();

        }
    }) 
}

getNewFreshAnime();
let currentScore = 0;
document.getElementById("current_score").innerHTML=currentScore;


function updateTitleContents(){

    var titleLeft = document.getElementById("anime_title_left");
    var titleRight = document.getElementById("anime_title_right");


    titleLeft.innerHTML = anime1.title;
    titleRight.innerHTML = anime2.title;


}


document.getElementById("higher").addEventListener('click', () => {
    
    if (anime2.popularity>=anime1.popularity) {
        waitDelay();
        currentScore = currentScore + 1;
        document.getElementById("current_score").innerHTML=currentScore;


        anime1 = anime2;
        newAnimeEntry()
        .then(result => {
            console.log('Nouvel anime :', result);
            // Faites ce que vous voulez avec le nouvel anime ici.
        })
        .catch(error => {
            console.error('Une erreur s\'est produite :', error);
        });



        updateTitleContents();

    }else{
        failure();
    }

});

document.getElementById("lower").addEventListener('click', () => {
    
    if (anime2.popularity<=anime1.popularity) {
        waitDelay();
        currentScore = currentScore + 1;
        document.getElementById("current_score").innerHTML=currentScore;




        anime1 = anime2;
        newAnimeEntry()
        .then(result => {
            console.log('Nouvel anime :', result);
            // Faites ce que vous voulez avec le nouvel anime ici.
        })
        .catch(error => {
            console.error('Une erreur s\'est produite :', error);
        });

        
        updateTitleContents();

    }else{
        failure();
    }

});




function waitDelay(){

        // Désactiver les interactions utilisateur en ajoutant un élément de superposition
        const overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    overlay.style.zIndex = "999";
    //document.body.appendChild(overlay);


        showPopularities();
        document.getElementById("click_module").style.visibility = "hidden";


         // Attendre 2 secondes avant de supprimer le message et l'overlay
    setTimeout(function () {
        hidePopularities();
        document.getElementById("click_module").style.visibility = "visible";

    }, 2000);

}


async function newAnimeEntry() {
    try {
        const response = await $.ajax({
            method: 'GET',
            url: 'http://127.0.0.1:8000/api/hol_n?rank=' + anime2.popularity + "&range_start=0.001&range_end=1000",
        });

        anime2 = response[0];

        // Mettez à jour les titres ici, une fois que les données pour anime2 sont disponibles
        updateTitleContents();

    } catch (error) {
        console.error('Une erreur s\'est produite :', error);
        throw error;
    }
}


function failure(){
    document.getElementById("defaite_screen").style.visibility = "visible";

    document.getElementById("replay_button").addEventListener('click', () => {
        getNewFreshAnime();
        let currentScore = 0;
        document.getElementById("current_score").innerHTML=currentScore;

        setTimeout(function () {
            document.getElementById("defaite_screen").style.visibility = "hidden";
        }, 2000);
        


    });

    document.getElementById("leave_button").addEventListener('click', () => {
        window.location.href = "http://127.0.0.1:8000/search/"
    });
}

function showPopularities(){

    left_pop = document.getElementById("anime_popularity_left");
    right_pop = document.getElementById("anime_popularity_right");

    left_pop.style.visibility = "visible";
    right_pop.style.visibility = "visible";

    left_pop.innerHTML = anime1.popularity;
    right_pop.innerHTML = anime2.popularity;


}


function hidePopularities(){
    left_pop = document.getElementById("anime_popularity_left");
    right_pop = document.getElementById("anime_popularity_right");

    left_pop.style.visibility = "hidden";
    right_pop.style.visibility = "hidden";
}


