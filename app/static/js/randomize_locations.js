const locations = [
[40.638839, -73.998195],
[40.574691, -73.983932],
[40.681387, -73.992881],
[40.711224, -73.961306],
[40.707454, -73.940271],
[40.697815, -73.951644],
[40.757756, -73.916107],
[40.774925, -73.913450],
[40.774200, -73.872296],
[40.759883, -73.832600],
[40.682984, -73.940768],
[40.631618, -73.953653],
[40.756136, -73.924013],
[40.7523199,-73.9130798],
[40.675841, -73.903128],
[40.756013, -73.944784],
[40.641708, -73.980471],
[40.599113, -73.951840],
[40.676839, -73.914155],
[40.700018, -73.916108],
[40.702240, -73.790950],
[40.746754, -73.891782],
[40.718373, -73.991775],
[40.664412, -73.940865]
]

function activateRandomize(button){
    button.style.display = "inline";
    button.onclick = function(){
        const location = locations[Math.floor(Math.random()*locations.length)];
        const coordsSelector = `#${button.classList[0]} input`
        const coords = document.querySelectorAll(coordsSelector);
        //const coords = button.parentNode.getElementsByTagName(button)
        coords[0].value = location[0];
        coords[1].value = location[1];
        const mapsLinkSelector = `#${button.classList[0]} .google-link a`
        const mapsLink = document.querySelector(mapsLinkSelector);
        mapsLink.href = `https://www.google.com/maps/place/${location[0]},${location[1]}`;
    }

}

function createGoogleMapsLink(div){
    const mapsLink = document.createElement('a');
    mapsLink.className = "btn btn-info"
    mapsLink.innerText = "See location in Google Maps";
    mapsLink.href = "#"
    const latlongs = div.getElementsByTagName("input")
    for (var i = 0; i < latlongs.length; i++) {
        latlongs[i].oninput = function(){
            mapsLink.href = `https://www.google.com/maps/place/${latlongs[0].value},${latlongs[1].value}`
        }
    }
    div.getElementsByClassName("google-link")[0].appendChild(mapsLink);
}


const coords = document.getElementsByClassName("location");
for (var i = 0; i < coords.length; i++) {
    createGoogleMapsLink(coords[i]); //second console output
}

const buttons = document.getElementsByClassName("randomize");
for (var i = 0; i < buttons.length; i++) {
    activateRandomize(buttons[i]); //second console output
}