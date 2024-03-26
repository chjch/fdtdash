// import { createRequire } from 'module';
// const require = createRequire(import.meta.url);
// import {I3SLoader} from "@loaders.gl/i3s";
// const I3SLoader= require("@loaders.gl/i3s");
// const { DeckGL, Tile3DLayer } = deck;
// const { I3SLoader } = loaders;

// import mapboxgl from 'mapbox-gl';
const { DeckGL, Tile3DLayer, FlyToInterpolator, COORDINATE_SYSTEM } = deck;
const { I3SLoader } = loaders;


const INITIAL_VIEW_STATE = {
    latitude: 37.9861,
    longitude: -100.9893,
    zoom: 11.88666637128745,
    pitch: 0
};

const deckgl = new DeckGL({
    container: "deckgl-container",
    mapStyle: "mapbox://styles/mapbox/dark-v11",
    initialViewState: INITIAL_VIEW_STATE,
    controller: true,
    onViewStateChange: ({viewState}) => {
        deckgl.setProps({
            viewState
        });
    },
    mapboxApiAccessToken: "pk.eyJ1IjoiY2hqY2giLCJhIjoiY2t0ZXA1aHYyMDBpczJvbXF0ODBoOHowdCJ9.vInEZlCBY3vMDQoiCjNNIw"
});


function renderLayers(opacity) {
    deckgl.setProps({
        layers: [
            new Tile3DLayer({
                id: "tile-3d-layer",
                data:
                    "https://tiles.arcgis.com/tiles/QCty4ZXRXx9qyVVL/arcgis/rest/services/NGA_Jacksonville_FL_Buildings_2010/SceneServer/layers/0",
                loadOptions: {
                    i3s: {
                        coordinateSystem: COORDINATE_SYSTEM.LNGLAT_OFFSETS
                    }
                },
                onTilesetLoad: (tileset) => {
                    const {zoom, cartographicCenter} = tileset;
                    const [longitude, latitude] = cartographicCenter || [];
                    const newViewState = {
                        zoom: zoom + 2.5,
                        latitude,
                        longitude,
                        transitionInterpolator: new FlyToInterpolator({speed: 1.5}),
                        transitionDuration: "auto"
                    };
                    // console.log(newViewState);
                    deckgl.setProps({
                        viewState: newViewState
                    });
                },
                loader: I3SLoader,
                pickable: true,
                autoHighlight: true
            })
        ]
    });
}

renderLayers();
