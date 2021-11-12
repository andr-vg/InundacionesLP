const initialLat=-34.9187;
const initialLong=-57.956;
const mapLayerUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';


export function Map(selector){
    let map;
    let marker;


    initializedMap(selector);


    function initializedMap(selector){
        map = L.map(selector).setView([initialLat,initialLong],13);
        L.tileLayer(mapLayerUrl).addTo(map);
    };


    function addListMarker(list){
        for(let i=0;i<list.length;i++){
            marker = new L.marker([list[i]["lat"],list[i]["long"]]).bindPopup(list[i]["name"]).addTo(map);
        }
    }

    return {
        addListMarker:addListMarker,
    };


}