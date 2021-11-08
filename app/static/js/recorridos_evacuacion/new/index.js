import { ZoneMap } from "../../ZoneMap.js";

const submitHandler = (event, map) => {
    event.preventDefault();

    if (!map.hasValidZone()) {
        alert('Debes dibujar una zona en el mapa.');
    }
    else{
        const name = document.querySelector('#name').value;
        const description = document.querySelector('#description').value;
        console.log(map.drawnlayers);
        const coordinates = map.drawnlayers[0].getLatLngs().flat().map(coordinate => {
            return { lat: coordinate.lat, lng: coordinate.lng }
        });

        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('coordinates', JSON.stringify(coordinates));

        fetch('recorridos_evacuacion', {
            method: 'POST',
            body: formData
        })
    }
}

window.onload = () => {
    const map = new ZoneMap({
        selector: 'mapid',
        addSearch: true,
    });
    const form = document.querySelector('#create-form');

    form.addEventListener('submit', (event) => submitHandler(event, map));
}