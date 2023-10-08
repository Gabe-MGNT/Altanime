



const anime_image = document.querySelector("div#left_panel img");
const most_colors = [];
const favorites_div = document.querySelector("#favorites");

anime_image.addEventListener('load', function() {
    var vibrant = new Vibrant(anime_image);
    var swatches = vibrant.swatches();
    
    for (var swatch in swatches) {
        if (swatches.hasOwnProperty(swatch) && swatches[swatch]) {
            //console.log(swatch, swatches[swatch].getHex());
            most_colors.push(swatches[swatch].getHex());
            //favorites_div.style.backgroundColor = swatches[swatch].getHex();
        }
    }
    console.log(most_colors);
    assignRandomColors();
});

const divIds = [
    'first_subrow',
    'favorites',
    'ranking',
    'populairty', // Assurez-vous que l'ID est correctement orthographié
    'aired_date',
    'themes',
    'genres',
    'type',
    'summary'
];


function assignRandomColors() {
    divIds.forEach(function (divId) {
        const randomIndex = Math.floor(Math.random() * most_colors.length);
        const randomColor = most_colors[randomIndex];
        document.querySelector(`#${divId}`).style.backgroundColor = randomColor;
        document.querySelector(`#${divId}`).style.color = getContrastColor(randomColor);
    });
}


function getContrastColor(hexColor) {
    // Convertissez la couleur hexadécimale en RGB
    const r = parseInt(hexColor.slice(1, 3), 16);
    const g = parseInt(hexColor.slice(3, 5), 16);
    const b = parseInt(hexColor.slice(5, 7), 16);

    // Calculez la luminance relative (Y)
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

    // Choisissez une couleur de police en fonction de la luminance
    return luminance > 0.5 ? "#473b31" : "#d2c5ba";
}



document.getElementById("third_row").addEventListener("click", () => {

    var recomm_panel = document.getElementById("summary_panel");

    recomm_panel.scrollIntoView({behavior: "smooth"});


})