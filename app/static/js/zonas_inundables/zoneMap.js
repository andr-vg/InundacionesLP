var mapOptions = {
    center: [-34.9187, -57.956],
    zoom: 10
 }

var map = new L.map('mapid', mapOptions);
var latlngs = coords
var polygon = L.polygon(latlngs, {color: color});
polygon.addTo(map);

var layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
map.addLayer(layer);