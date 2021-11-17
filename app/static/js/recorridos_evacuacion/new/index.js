import { ZoneMap } from "../../ZoneMap.js";

const submitHandler = (event, map) => {
    

    if (!map.hasPoints() || !map.hasValidZone()) {
        event.preventDefault();
        alert('Debes dibujar al menos 3 puntos en el mapa.');
    }
    else{
        const coordinates = [];
        for (let coord of map.drawnLayers) {
            coordinates.push([coord['lat'], coord['lng']]);
        }
        document.getElementById('coordinates').setAttribute('value', JSON.stringify(coordinates));
    }
}

window.onload = () => {
    const map = new ZoneMap({
        selector: 'mapid',
        addSearch: true,
    });
    const form = document.querySelector('#create-form');
    //var pointA = new L.LatLng(28.635308, 77.22496);
    //var pointB = new L.LatLng(28.984461, 77.70641);
    //var pointList = [pointA, pointB];

    form.addEventListener('submit', (event) => submitHandler(event, map));
}