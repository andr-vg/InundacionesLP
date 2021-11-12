// constantes

const initialLat = -34.9187;
const initialLng = -57.956;
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

export class ZoneMap {
    #drawnItems;

    constructor({ selector }) {
        this.#drawnItems = new L.FeatureGroup();

        this.#initializeMap(selector);
        
        this.map.on(L.Draw.Event.CREATED, (e) => {
            this.#eventHandler(e, this.map, this.#drawnItems, this.editControls, this.createControls)
        });
        this.map.on('draw:deleted', () => {
            this.#deleteHandler(this.map, this.editControls, this.createControls)
        });
    }

    #initializeMap(selector) {
        this.map = L.map(selector).setView([initialLat, initialLng], 13);
        L.tileLayer(mapLayerUrl).addTo(this.map);

        this.map.addLayer(this.#drawnItems);
        
        const coords = document.querySelector('#coordinates').value; 
        if (coords == ""){
            this.map.addControl(this.createControls);
        }else{
            const coordinates = JSON.parse(coords);
            
            var polyline = L.polyline(coordinates).addTo(this.map);  
            this.#drawnItems.addLayer(polyline);
            this.map.fitBounds(this.#drawnItems.getBounds());
            this.map.addControl(this.editControls);
        }
        
        //var polyline = L.polyline([[-65.10418, -26.62987],[-35.19738, -16.875], [9.9804, 121.9189]]).addTo(this.map);
        //this.#drawnItems.addLayer(polyline);
        //this.map.fitBounds(this.#drawnItems.getBounds());
        //console.log(this.drawnLayers);
        //this.map.addControl(this.createControls);
        //this.map.addControl(this.editControls);
    }

    #eventHandler(e, map, drawnItems, editControls, createControls) {
        const existingZones = Object.values(drawnItems._layers);

        if (existingZones.length == 0) {
            const type = e.layerType;
            const layer = e.layer;

            if (type == 'marker') {
                // do marker specific actions
                // currently markers are disabled
            }
            layer.editing.enable();
            drawnItems.addLayer(layer);
            editControls.addTo(map);
            createControls.remove();
        }
    };

    #deleteHandler(map, editControls, createControls) {
        createControls.addTo(map);
        editControls.remove();
    }

    hasValidZone() {
        return this.drawnLayers.length >= 3;
    }

    get drawnLayers() {
        const results = Object.values(this.#drawnItems._layers);
        //return Object.values(this.#drawnItems._layers);
        return results[0]._latlngs;
    }

    get editControls() {
        return this.editControlsToolbar ||= new L.Control.Draw({
            draw: false,
            edit: {
                featureGroup: this.#drawnItems
            }
        });
    }

    get createControls() {
        return this.createControlsToolbar ||= new L.Control.Draw({
            draw: {
                circle: false,
                marker: false,
                polyline: true,
                polygon: false,
                rectangle: false,
                circlemarker: false,
            }
        });
    }
}

