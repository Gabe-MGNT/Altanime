
var anime1;
var anime2;
let currentScore = 0;

function getNewRandomAnime(){
    $.ajax({
        method: 'GET',
        url : 'http://127.0.0.1:8000/api/random?samples=2',
        success: function(response) {
            anime1 = response[0];
            anime2 = response[1];
            
            if (anime1.image == null) {
                document.getElementById("left_pic").src = "../static/img/default_template.png";
            }else{
                document.getElementById("left_pic").src = anime1.image;
            }

            if (anime2.image == null) {
                document.getElementById("right_pic").src = "../static/img/default_template.png";
            }else{
                document.getElementById("right_pic").src = anime2.image;
            }

            updateTitleContents();


        }
    }) 
}

// When page loads (start a game)
function startGame(){
    getNewRandomAnime();

    currentScore = 0;
    document.getElementById("current_score").innerHTML=currentScore;
    document.getElementById("best_score").innerHTML=currentScore;

}

window.onload = function () {
    if (localStorage.getItem("hasCodeRunBefore") === null) {
        startGame();
        localStorage.setItem("hasCodeRunBefore", true);
    } else if (performance.navigation.type === 1) {
        // La page a été rechargée (rafraîchie)
        startGame();
    }
}



function updateTitleContents(){

    var titleLeft = document.getElementById("anime_title_left");
    var titleRight = document.getElementById("anime_title_right");


    titleLeft.innerHTML = anime1.title;
    titleRight.innerHTML = anime2.title;


}


document.getElementById("higher").addEventListener('click', () => {
    
    if (anime2.popularity>=anime1.popularity) {
        waitingNextRound();
        currentScore = currentScore + 1;
        document.getElementById("current_score").innerHTML=currentScore;


        anime1 = {...anime2};
        nextRound()
        .then(result => {
            console.log('Nouvel anime :', result);
            // Faites ce que vous voulez avec le nouvel anime ici.
            updateTitleContents();
            slideBothPictures();
        })
        .catch(error => {
            console.error('Une erreur s\'est produite :', error);
        }, {once:true});






    }else{
        failure();
    }

});

document.getElementById("lower").addEventListener('click', () => {
    
    

    if (anime2.popularity<=anime1.popularity) {
        waitingNextRound();

        currentScore = currentScore + 1;
        document.getElementById("current_score").innerHTML=currentScore;

        anime1 = {...anime2};

        nextRound()
        .then(result => {
            console.log('Nouvel anime :', result);
            updateTitleContents();
            slideBothPictures();
            // Faites ce que vous voulez avec le nouvel anime ici.
        })
        .catch(error => {
            console.error('Une erreur s\'est produite :', error);
        }, {once:true});



    }else{
        failure();
    }

});



function slideRightPictures(){
    img_right = document.getElementById("right_pic");
    img_right.classList.remove("right_added_img");
    img_right.classList.add("right_removed_img");

    img_right2 = document.getElementById("right_replacement_pic");

    if (anime2.image == null){
        img_right2.src = "../static/img/default_template.png";
    }else{
        img_right2.src = anime2.image;
    }

    img_right2.style.visibility = "visible";
    img_right2.classList.add("right_added_img");

    setTimeout(function () {
        img_right.remove();

        img_right2.id = "right_pic";

        const newImgRight = document.createElement("img");
        newImgRight.id = "right_replacement_pic";



        img_right2.parentNode.insertBefore(newImgRight, img_right2.nextSibling);

    }, 2000);

}

function slideLeftPictures(){
    img_left = document.getElementById("left_pic");
    img_left.classList.remove("left_added_img");
    img_left.classList.add("left_removed_img");

    img_left2 = document.getElementById("left_replacement_pic");

    
    if (anime1.image == null){
        img_left2.src = "../static/img/default_template.png";
    }else{
        img_left2.src = anime1.image;
    }

    img_left2.style.visibility = "visible";
    img_left2.classList.remove("left_removed_img");
    img_left2.classList.add("left_added_img");

    setTimeout(function () {
        img_left.remove();

        img_left2.id = "left_pic";

        const newImgLeft = document.createElement("img");
        newImgLeft.id = "left_replacement_pic";


        img_left2.parentNode.insertBefore(newImgLeft, img_left2.nextSibling);
    }, 2000);

}


function slideBothPictures (){
    slideLeftPictures();
    slideRightPictures();
}



function waitingNextRound(){

        showPopularities();
        document.getElementById("choosing_module").style.visibility = "hidden";


         // Attendre 2 secondes avant de supprimer le message et l'overlay
    setTimeout(function () {
        hidePopularities();
        document.getElementById("choosing_module").style.visibility = "visible";

    }, 2000);

}


async function nextRound() {
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
    document.getElementById("defaite_screen").style.zIndex = "5";
    document.getElementById("defaite_screen").classList.remove("defeat_screen_hidden");
    document.getElementById("defaite_screen").classList.add("defeat_screen_shown");


    document.getElementById("replay_button").addEventListener('click', () => {
        startGame();

        document.getElementById("defaite_screen").classList.remove("defeat_screen_shown");
        document.getElementById("defaite_screen").classList.add("defeat_screen_hidden");

        setTimeout(function () {
            document.getElementById("defaite_screen").style.zIndex = "-1";
        }, 2000);

        


    }, {once:true});

    document.getElementById("leave_button").addEventListener('click', () => {
        window.location.href = "http://127.0.0.1:8000/search/"
    }, {once:true});
}


function updatePopularities(){
    left_pop = document.getElementsByClassName("anime_left_ranking")[0];
    right_pop = document.getElementsByClassName("anime_right_ranking")[0];

    left_pop.innerHTML = anime1.popularity;
    right_pop.innerHTML = anime2.popularity;
}

function showPopularities(){

    updatePopularities();

    left_pop = document.getElementById("left_ranking");
    right_pop = document.getElementById("right_ranking");

    left_pop.style.visibility = "visible";
    right_pop.style.visibility = "visible";


}


function hidePopularities(){
    left_pop = document.getElementById("right_ranking");
    right_pop = document.getElementById("left_ranking");

    left_pop.style.visibility = "hidden";
    right_pop.style.visibility = "hidden";
}


