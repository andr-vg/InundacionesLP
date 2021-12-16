// constantes: los puntos del mapa
const latlngs = JSON.parse(document.querySelector('#coordinates').value); 

// Creating map options
var mapOptions = {
    center: latlngs[0],
    zoom: 13
 }
 var map = new L.map('mapid', mapOptions); // Creating a map object
 
 // Creating a Layer object
 var layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
 map.addLayer(layer);      // Adding layer to the map
 
 // Creating markers
 var hydMarker = new L.Marker([17.385044, 78.486671]);
 var vskpMarker = new L.Marker([17.686816, 83.218482]);
 var vjwdMarker = new L.Marker([16.506174, 80.648015]);
 
 // Creating latlng object
 var coords = L.polyline(latlngs, {color: 'red'}); // Creating a polyline
 
 // Creating feature group
 var featureGroup = L.featureGroup([coords]);
 featureGroup.setStyle({color:'blue',opacity:.5});
 featureGroup.bindPopup("Coordenadas del recorrido");
 featureGroup.addTo(map);      // Adding layer group to map