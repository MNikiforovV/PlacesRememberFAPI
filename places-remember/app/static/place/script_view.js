
let mapOptions = {
    center:[
        document.getElementById('latitude').value, 
        document.getElementById('longitude').value
    ],
    zoom:10
}

let map = new L.map('map' , mapOptions);

let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
map.addLayer(layer);


let marker = new L.Marker([
    document.getElementById('latitude').value, 
    document.getElementById('longitude').value
])
marker.addTo(map);