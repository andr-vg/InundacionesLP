const initialLat=-34.9187;
const initialLong=-57.956;
const mapLayerUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';


export function Map(selector){
    let marker;
    let map;



    initializedMap(selector);



    map.addEventListener('click',(e) => { addMarker(e.latlng)});


    function initializedMap(selector){
        map = L.map(selector).setView([initialLat,initialLong],13);
        L.tileLayer(mapLayerUrl).addTo(map);
    };


    function addMarker({lat,lng}){
        if(marker){
            marker.remove();
        };
        marker = L.marker([lat,lng]).addTo(map);
    };


    return {
        get marker() { return marker },
        addMarker: addMarker
    };


}