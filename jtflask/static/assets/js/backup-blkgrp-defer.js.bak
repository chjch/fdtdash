let isGeoJSONLoaded = false;

const geojsonLayer = new deck.GeoJsonLayer({
    data: (
        'https://taurus.at.geoplan.ufl.edu/arcgis/rest/services/fgdl/USCB/Mapserver/10/' +
        'query?where=COUNTY=31&outFields=TOTALPOP,GEOID20&f=geojson'
    ),
    opacity: 0.2,
    stroked: true,
    filled: true,
    extruded: true,
    wireframe: false,
    fp64: true,
    getElevation: f => Math.sqrt(f.properties.TOTALPOP) * 100,
    getFillColor: f => [255, 255, 255, 255], // colorScale(f.properties.TOTALPOP),
    getLineColor: f => [0, 0, 0],
    getLineWidth: 2,
    pickable: true,
    // onDataLoad: () => {
    //     deckgl.setProps({
    //         viewState: newViewState
    //     });
    // }
    onClick: ({layer, object}) => {
        const {viewport} = layer.context;
        const [xmin, ymin, xmax, ymax] = turf.bbox(object);
        const {longitude, latitude, zoom} = viewport.fitBounds(
            [[xmin, ymin], [xmax, ymax]],
            {
                width: 400,
                height: 400
            }
        );
        deckgl.setProps({
            viewState: {
                longitude,
                latitude,
                zoom: zoom-1,
                pitch: 45,
                transitionInterpolator: new deck.FlyToInterpolator(),
                transitionDuration: "auto"
            }
        });
        // console.log('Clicked:', object);
        // document.getElementById("GEOID20").attributes[1].value = object.properties.GEOID20;
        // console.log(document.getElementById("deckgl-container"));
        document.getElementById("deckgl-container").setAttribute("data-geoid20", object.properties.GEOID20);
        // document.getElementById("means-to-work-title").innerHTML = object.properties.GEOID20;
        // console.log(document.getElementById("GEOID20").attributes[4].value);
    }
});

const INITIAL_VIEW_STATE = {
    latitude: 49.254,
    longitude: -123.13,
    zoom: 11,
    maxZoom: 16,
    pitch: 0
};

const newViewState = {
    zoom: 8,
    latitude: 30.325577,
    longitude: -81.651584,
    pitch: 0,
    transitionInterpolator: new deck.FlyToInterpolator(),
    transitionDuration: "auto"
};

const deckgl = new deck.DeckGL({
    container: "deckgl-container",
    mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
    initialViewState: newViewState,
    controller: true,
    onViewStateChange: ({viewState}) => {
        deckgl.setProps({
            viewState
        });
    },
    mapboxApiAccessToken: "pk.eyJ1IjoiY2hqY2giLCJhIjoiY2t0ZXA1aHYyMDBpczJvbXF0ODBoOHowdCJ9.vInEZlCBY3vMDQoiCjNNIw",
    layers: [geojsonLayer],
    getTooltip
});


// setTimeout(() => {
//     deckgl.setProps({
//         viewState: newViewState
//     });
//     // Code to run after delay
// }, 1000);


const COLOR_SCALE = [
    // negative
    [65, 182, 196],
    [127, 205, 187],
    [199, 233, 180],
    [237, 248, 177],

    // positive
    [255, 255, 204],
    [255, 237, 160],
    [254, 217, 118],
    [254, 178, 76],
    [253, 141, 60],
    [252, 78, 42],
    [227, 26, 28],
    [189, 0, 38],
    [128, 0, 38]
];

function colorScale(x) {
    const i = Math.round(x/5000 * 7) + 4;
    if (x < 0) {
        return COLOR_SCALE[i] || COLOR_SCALE[0];
    }
    return COLOR_SCALE[i] || COLOR_SCALE[COLOR_SCALE.length - 1];
}

function getTooltip({object}) {
    return object && `TOTALPOP
${object.properties.TOTALPOP}
Growth
${Math.round(object.properties.growth * 100)}`;
}