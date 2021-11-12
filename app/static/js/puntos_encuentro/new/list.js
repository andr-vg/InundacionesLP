import { Map } from '../../ListMarkerMap.js';

window.onload = () => {
    const map = new Map('mapid');
    let list_coords = JSON.parse(document.querySelector('#puntos_encuentro_list').value);
    map.addListMarker(list_coords);
}