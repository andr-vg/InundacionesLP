import { ZoneMap } from "../../ZoneMap.js";

const submitHandler = (event, map) => {
    event.preventDefault();

    if (!map.hasValidZone()) {
        alert('Debes dibujar al menos 3 puntos en el mapa.');
    }
    else{
        const name = document.querySelector('#name').value;
        const description = document.querySelector('#description').value;
        const csrf_token = document.querySelector('#csrf_token').value;        
        //var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map)
        //const coordinates = map.drawnlayers[0].getLatLngs().flat().map(coordinate => {
        //    return { lat: coordinate.lat, lng: coordinate.lng }
        //});
        const coordinates = [];
        for (let coord of map.drawnLayers) {
            coordinates.push([coord['lat'], coord['lng']]);
        }
        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('coordinates', JSON.stringify(coordinates));
        formData.append('csrf_token', csrf_token);

        fetch('/recorridos_evacuacion', {
            method: 'POST',
            body: formData
        })
        .then((response)=>{         
            if(response.redirected){
                var msj = document.querySelector("flashes");
                window.location.href = response.url;
                
                alert("El recorrido ha sido creado con éxito.");
                
            }
            else{
                var msj = document.querySelector("flashes");
                alert("El nombre ya existe, ingrese otro.");
            }
            
        })           
        .catch(function(e){
            
        })     
        
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