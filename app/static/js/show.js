import { Map } from './ShowMapMaker.js';



window.onload = () => {
    const map = new Map('mapid');
    let lat = document.getElementById("lat").getAttribute("value");
    let lng = document.getElementById("long").getAttribute("value");
    map.addMarker({lat,lng});
}