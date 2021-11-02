import { Map } from '../../MapMaker.js';

const submitHandler = (event, map) =>{
    if(!map.marker){
        event.preventDefault();
        alert("Se debe seleccionar una ubicacion en el mapa");
    }
    else{
        document.getElementById('lat').setAttribute('value', map.marker.getLatLng().lat);
        document.getElementById('long').setAttribute('value', map.marker.getLatLng().lng);
    }
}

window.onload = () => {
    const map = new Map('mapid');
    const form = document.getElementById("create-denuncia");
    form.addEventListener('submit',(event) => submitHandler(event,map));
}